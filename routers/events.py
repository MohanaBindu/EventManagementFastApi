from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from routers import events
from schemas import PostEventBase, PostEventDisplay, AttendeeBase, AttendeeDisplay
from database.database import get_db
from database.events_db import create_event, get_all_events, post_register_user, get_all_attendees


router = APIRouter(
    prefix = "/events",
    tags = ["events"])

@router.post("/", response_model=PostEventDisplay, status_code=status.HTTP_201_CREATED)
async def add_event(request: PostEventBase, db: AsyncSession = Depends(get_db)):
    """Create a new event"""
    try:
        return await create_event(request, db)
    except ValueError as e:
       raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST,
             detail=str(e))
       

@router.get("/", response_model= List[PostEventDisplay])
async def all_events(db:AsyncSession = Depends(get_db)):
    """Get all events"""
    events = await get_all_events(db)
    if not events:
       raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No Events found")
    return events


@router.post("/{event_id}/register", response_model=AttendeeDisplay, status_code=status.HTTP_201_CREATED)
async def add_attendee(event_id:int, request: AttendeeBase, db:AsyncSession = Depends(get_db)):
    """Register an attendee for an event"""
    try:
       return await post_register_user(event_id, request, db)
    except ValueError as e:
       raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST,
       detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to register attendee"
        )


@router.get("/{event_id}/attendees", response_model = List[AttendeeDisplay])
async def get_attendees(event_id:int, db:AsyncSession= Depends(get_db)):
    """Get all attendees for a specific event"""
    attendees = await get_all_attendees(event_id,db)
    if not attendees:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No attendees found for this event"
            )
    return attendees
    