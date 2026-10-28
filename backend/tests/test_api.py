from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200


def test_incidents_endpoint():
    response = client.get("/api/incidents")
    assert response.status_code == 200
    assert response.headers["content-type"].startswith("application/json")