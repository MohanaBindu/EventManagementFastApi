from fastapi import FastAPI
from database import models
from database.database import engine
from routers import events

app = FastAPI()
app.include_router(events.router)



# models.Base.metadata.create_all(engine)