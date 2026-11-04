from fastapi.testclient import TestClient

from app.main import testapp

client = TestClient(testapp)

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
