from pydantic import BaseModel
from datetime import datetime


# POST /events
# Creates a new event with fields: name, location, start_time, end_time, max_capacity

class PostEventBase(BaseModel):
    name: str
    location: str
    start_time : datetime
    end_time: datetime
    max_capacity: int


class PostEventDisplay(BaseModel):
    name: str
    location: str
    start_time : datetime
    end_time: datetime
    max_capacity: int   
    class Config():
        orm_mode = True

class AttendeeBase(BaseModel):
    name: str
    email: str
    


class AttendeeDisplay(AttendeeBase):
    id: int
    class Config:
        orm_mode = True
    



# GET /events
# Lists all upcoming events


