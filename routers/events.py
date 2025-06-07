from fastapi import APIRouter, Depends
from sqlalchemy.orm import session
from routers import events
from schemas import PostEventBase, PostEventDisplay, AttendeeBase, AttendeeDisplay
from database.database import get_db
from database.events_db import create_event, get_all_events, post_register_user, get_all_attendees


router = APIRouter(
    prefix = "/events",
    tags = ["events"])

@router.post("/events", response_model=PostEventDisplay)
def add_event(request: PostEventBase, db: session = Depends(get_db)):
    return create_event(request, db)


@router.get("/events")
def all_events(db:session = Depends(get_db)):
    return get_all_events(db)


@router.post("/events/{event_id}/register", response_model=AttendeeDisplay)
def add_attendee(event_id:int, request: AttendeeBase, db:session = Depends(get_db)):
    return post_register_user(event_id, request, db)

@router.get("/events/{event_id}/attendees")
def get_attendees(event_id:int, db:session= Depends(get_db)):
 return get_all_attendees(event_id,db)
    