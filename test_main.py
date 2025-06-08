from fastapi.testclient import TestClient
from main import app
from datetime import datetime,timedelta

client = TestClient(app)


TEST_EVENT = {
    "name": "Python Conference",
    "location": "Virtual",
    "start_time": (datetime.now() + timedelta(days=1)).isoformat(),
    "end_time": (datetime.now() + timedelta(days=2)).isoformat(),
    "max_capacity": 100
}


def test_get_events_success():
    response = client.get("/events")
    assert response.status_code == 200


def test_post_event_success():
     """Test successful event creation"""
     response = client.post("/events", json=TEST_EVENT)
     assert response.status_code == 201
     data = response.json()
     print(data)
     assert data["name"] == TEST_EVENT["name"]

def test_create_event_invalid_capacity():
    """Test capacity must be positive"""
    invalid_event = TEST_EVENT.copy()
    invalid_event["max_capacity"] = 0
    response = client.post("/events", json=invalid_event)
    assert response.status_code == 400
    assert "Capacity must be positive" in str(response.json())

    
