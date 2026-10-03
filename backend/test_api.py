import pytest
from fastapi.testclient import TestClient
from main import app
from datetime import datetime

client = TestClient(app)

def test_health_check():
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"

def test_get_analytics():
    response = client.get("/api/analytics")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) >= 2

def test_submit_review():
    payload = {
        "id": 3,
        "title": "The Midnight Manuscript",
        "status": "pending",
        "score": 7.8,
        "timestamp": datetime.now().isoformat()
    }
    response = client.post("/api/reviews", json=payload)
    assert response.status_code == 200
    assert response.json()["title"] == "The Midnight Manuscript"
    
    # Verify it was added to the store
    get_response = client.get("/api/analytics")
    assert any(item["id"] == 3 for item in get_response.json())