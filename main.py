from fastapi import FastAPI, Form,File, UploadFile
from db import events_collection
from pydantic import BaseModel
from bson.objectid import ObjectId
from utils import replace_mongo_id
from typing import Annotated
import cloudinary
import cloudinary.uploader
import cloudinary.api


# Configure Cloudinary
cloudinary.config(
    cloud_name="dhqwkwo8e",
    api_key="544878511352217",
    api_secret="DB2whHclPE2tpDECsKPQNRq7G0Y"
)

class EventModel(BaseModel):
    title: str
    description: str


app = FastAPI()

 
@app.get("/")
def get_home():
    return {"message": "you are on the home page"}


# Events endpoints
@app.get("/events")
def get_events(title="", description="", limit=10, skip=0):
    # get all events from the database
    events = events_collection.find(
        filter={
            "$or": [
                {"title": {"$regex": title, "$options": "i"}},
                {"description": {"$regex": description, "$options": "i"}},
            ]
        },
        limit=int(limit),
        skip=int(skip)
    ).to_list()
    # returns response
    return {"data": list(map(replace_mongo_id, events))}


@app.post("/events")
def post_event(
    title: Annotated[str, Form()], 
    description: Annotated[str, Form()],
    flyer: Annotated[UploadFile, File()]):
    # upload flyer to cloudinary
    upload_result = cloudinary.uploader.upload(flyer.file)
    print(upload_result)  # Debugging line to check upload result
    # insert the event into the database
    events_collection.insert_one({
        "title": title,
        "description": description,
        "flyer_url": upload_result.get("secure_url")
    })
    # events_collection.insert_one(event.model_dump())
    return {"message": "Event added successfully"}


@app.get("/events/{event_id}")
def get_event_by_id(event_id):
    # Get event from database by id
    event = events_collection.find_one({"_id": ObjectId(event_id)})
    # Return response
    return {"data": replace_mongo_id(event)}
