from .models import EventManagemnet, Attendees
from schemas import PostEventBase,PostEventDisplay, AttendeeBase
from sqlalchemy.orm.session import Session
import datetime
from database.models import EventManagemnet,Attendees
from fastapi import HTTPException, status

def create_event(request: PostEventBase, db:Session):
    new_event= EventManagemnet(
    name = request.name,
    location = request.location,
    start_time = request.start_time,
    end_time = request.end_time,
    max_capacity = request.max_capacity, 
    )
    db.add(new_event)
    db.commit()
    db.refresh(new_event)
    return new_event

def get_all_events(db:Session):
    return db.query(EventManagemnet).all()

# POST /events/{event_id}/register

def post_register_user(event_id:int, request: AttendeeBase, db:Session):
    event =  db.query(EventManagemnet).filter(EventManagemnet.id==event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not fount")
    attendee_count =  db.query(Attendees).filter(Attendees.event_id==event_id).count()
    if attendee_count>=event.max_capacity:
        raise HTTPException(status_code=500, detail="Event is full booked")
    new_attendee = Attendees(
        name = request.name,
        email = request.email,
        event_id = event_id,
    )
    db.add(new_attendee)
    db.commit()
    db.refresh(new_attendee)
    return new_attendee

def get_all_attendees(event_id:int, db:Session):
    all_attendees = db.query(Attendees).filter(Attendees.event_id==event_id).all()
    return all_attendees









