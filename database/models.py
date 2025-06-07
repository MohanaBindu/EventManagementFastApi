from .database import Base
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey



# Creates a new event with fields: name, location, start_time, end_time, max_capacity

class EventManagemnet(Base):
    __tablename__ = "Events"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    location = Column(String)
    start_time = Column(DateTime)
    end_time = Column(DateTime) 
    max_capacity = Column(Integer)


# Registers an attendee (name, email) for a specific event
class Attendees(Base):
    __tablename__= "EventAttendee"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String)
    event_id = Column(Integer, ForeignKey("Events.id"))

