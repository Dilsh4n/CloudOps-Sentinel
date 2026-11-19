from fastapi.testclient import TestClient
from prometheus_client.parser import text_string_to_metric_families

from app.main import app

client = TestClient(app)

def test_home_endpoint():
    response = client.get("/")

    assert response.status_code == 200

    data = response.json()

    assert data["application"] == "CloudOps Sentinel"
    assert data["message"] == "API is running"



def test_health_endpoint():
    response = client.get("/health")

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "healthy"
    assert "timestamp" in data


def get_counter_value():
    response = client.get("/metrics")

    assert response.status_code == 200

    # Parse Prometheus metrics output
    for family in text_string_to_metric_families(response.text):
        for sample in family.samples:

            if (
                sample.name == "sentinel_http_requests_total"
                and sample.labels == {
                    "method": "GET",
                    "route": "/health",
                    "status": "200",
                }
            ):
                return sample.value

    return 0.0


def test_metrics_counter():
    # Get the initial counter value
    initial_count = get_counter_value()

    # Send 5 HTTP requests
    for _ in range(5):
        response = client.get("/health")
        assert response.status_code == 200

    # Get the updated counter value
    final_count = get_counter_value()

    # Verify exactly 5 new requests were recorded
    assert final_count - initial_count == 5