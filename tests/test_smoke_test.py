from unittest.mock import Mock
import requests
from scripts.smoke_test import check_health

def test_healthy_response(monkeypatch):
    response = Mock()
    response.status_code = 200
    response.json.return_value = {
        "status": "healthy",
        "timestamp": "2026-11-03T16:00:21.581566+00:00"
    }

    # Replace the real HTTP GET function
    def fake_get(url, timeout):
        assert url == "http://example.test:8000/health"
        assert timeout == 5
        return response

    monkeypatch.setattr(
        "scripts.smoke_test.requests.get",
        fake_get
    )

    result = check_health("http://example.test:8000/", 5)
    assert result is True

def test_http_error(monkeypatch):
    response = Mock()
    response.status_code = 500

    monkeypatch.setattr(
        "scripts.smoke_test.requests.get",
        lambda url, timeout: response
    )

    result = check_health("http://example.test:8000", 5)
    assert result is False


def test_unhealthy_application(monkeypatch):
    response = Mock()
    response.status_code = 200
    response.json.return_value = {
        "status": "unhealthy"
    }

    monkeypatch.setattr(
        "scripts.smoke_test.requests.get",
        lambda url, timeout: response
    )

    result = check_health("http://example.test:8000", 5)
    assert result is False


def test_connection_failure(monkeypatch):
    def fake_get(url, timeout):
        raise requests.exceptions.ConnectionError(
            "Connection refused"
        )

    monkeypatch.setattr(
        "scripts.smoke_test.requests.get",
        fake_get
    )

    result = check_health("http://example.test:8000", 5)
    assert result is False