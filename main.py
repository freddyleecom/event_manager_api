from fastapi import FastAPI
from db import events_collection
from pydantic import BaseModel

class EventModel(BaseModel):
    title: str
    description: str
    

app = FastAPI()


@app.get("/")
def get_home():
    return {"message": "you are on the home page"}  

# Events endpoints
@app.get("/events")
def get_events():
    # get all events from the database
    events = events_collection.find().to_list()
    # returns response
    return {"data": events}

@app.post("/events")
def create_event(event: EventModel):
    # insert the event into the database
    events_collection.insert_one(event.model_dump)
    return {"message": "Event added successfully"}

@app.get("/events/{event_id}")
def get_event_by_id(event_id):
    return {"data": {"id": event_id}}

@app.get("/events/{event_id}")
def get_event_by_id(event_id):
    # Get event from database by id
    event = events_collection.find_one({"_id": event_id})
    # Return response
    return {"data": event}