import pytest
from datetime import datetime, timedelta
from database.models import EventManagement, Attendees
from sqlalchemy.orm import Session
from database.database import get_db

# ---- Fixtures ----
@pytest.fixture
def db_session(client):
    # Yield a new DB session for each test
    db: Session = next(get_db())
    yield db
    db.rollback()  # Cleanup after test

@pytest.fixture
def sample_event(db_session: Session):
    # Create a reusable test event
    event = EventManagement(
        name="TechConf",
        location="Bangalore",
        start_time="2025-06-10T10:00:00",
        end_time="2025-06-10T12:00:00",
        max_capacity=2
    )
    db_session.add(event)
    db_session.commit()
    return event

# ---- Tests ----
def test_register_attendee_success(client, db_session, sample_event):
    response = client.post(
        f"/events/{sample_event.id}/register",
        json={"name": "John", "email": "john@example.com"}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "John"
    assert data["email"] == "john@example.com"
    assert data["event_id"] == sample_event.id

    # Verify DB record
    attendee = db_session.query(Attendees).filter_by(event_id=sample_event.id).first()
    assert attendee is not None

def test_register_attendee_overbook(client, db_session, sample_event):
    # Fill capacity
    client.post(
        f"/events/{sample_event.id}/register",
        json={"name": "Jane", "email": "jane@example.com"}
    )

    # Attempt overbooking
    response = client.post(
        f"/events/{sample_event.id}/register",
        json={"name": "Bob", "email": "bob@example.com"}
    )
    
    assert response.status_code == 400
    assert response.json()["detail"] == "Event is fully booked"