from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "OK"}

def test_readiness_check():
    response = client.get("/readiness")
    assert response.status_code == 200
    assert response.json() == {"status": "ready"}

# Add more test functions for other endpoints here