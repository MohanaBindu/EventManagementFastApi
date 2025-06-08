from .models import EventManagemnet, Attendees
from schemas import PostEventBase,PostEventDisplay, AttendeeBase
# from sqlalchemy.orm.session import Session
from sqlalchemy.ext.asyncio import AsyncSession
import datetime
from sqlalchemy import select, func
from database.models import EventManagemnet,Attendees
from fastapi import HTTPException, status, Depends
from typing import List
from database.database import get_db

async def create_event(request: PostEventBase, db: AsyncSession)-> EventManagemnet:
    """
    Create a new event in the database
    Args:
        request: PostEventBase - Event data
        db: Session - Database session
    Returns:
        EventManagemnet: The created event
    Raises:
        HTTPException: If validation fails
    """
    if request.max_capacity <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Capacity must be positive"
        )
    try:
        new_event= EventManagemnet(
        name = request.name,
        location = request.location,
        start_time = request.start_time,
        end_time = request.end_time,
        max_capacity = request.max_capacity, 
        )
        db.add(new_event)
        await db.commit()
        await db.refresh(new_event)
        return new_event
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create event: {str(e)}"
        )

async def get_all_events(db: AsyncSession)->List[EventManagemnet]:
    """
    Get all events from the database
    Args:
        db: Session - Database session
    Returns:
        List[EventManagemnet]: List of all events
    """
     
    result = await db.execute(select(EventManagemnet))
    events = result.scalars().all()
    return events
    #   result = await db.query(EventManagemnet).all()
    #  return result

# POST /events/{event_id}/register

async def post_register_user(event_id:int, request: AttendeeBase, db: AsyncSession)->Attendees:
    """
    Register a new attendee for an event
    Args:
        event_id: int - ID of the event
        request: AttendeeBase - Attendee data
        db: Session - Database session
    Returns:
        Attendees: The created attendee record
    Raises:
        HTTPException: If event not found or capacity full
    """
    try:
        # Validate event exists
        result = await db.execute(select(EventManagemnet).where(EventManagemnet.id==event_id))
        event  = result.scalar_one_or_none()
        if not event:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Event not found"
            )
        result = await db.execute(
            select(func.count()).select_from(Attendees).where(Attendees.event_id == event_id)
        )
        attendee_count = result.scalar()
        if attendee_count>=event.max_capacity:
            raise HTTPException(status_code=500, detail="Event is full booked")
        new_attendee = Attendees(
            name = request.name,
            email = request.email,
            event_id = event_id,
        )
        db.add(new_attendee)
        await db.commit()
        await db.refresh(new_attendee)
        return new_attendee
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Registration failed: {str(e)}"
        )

async def get_all_attendees(event_id:int, db: AsyncSession)->List[Attendees]:
    """
    Get all attendees for a specific event
    Args:
        event_id: int - ID of the event
        db: Session - Database session
    Returns:
        List[Attendees]: List of attendees
    Raises:
        HTTPException: If event doesn't exist"""
    result  = await db.execute(select(Attendees).where(Attendees.event_id==event_id))
    attendees = result.scalars().all()
    if not attendees:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event not found"
        )
    return attendees









