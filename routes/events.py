from fastapi import Form, File, UploadFile, HTTPException, status, APIRouter, Depends
from db import events_collection
from bson.objectid import ObjectId
from utils import replace_mongo_id
from typing import Annotated
import cloudinary
import cloudinary.uploader
from dependencies.authn import is_authenticated
from dependencies.authz import has_roles


# Create event router
events_router = APIRouter()


# Events endpoints
@events_router.get("/events")
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
        skip=int(skip),
    ).to_list()
    # returns response
    return {"data": list(map(replace_mongo_id, events))}


@events_router.post("/events", dependencies=[Depends(has_roles(["host","admin"]))])
def post_event(
    title: Annotated[str, Form()],
    description: Annotated[str, Form()],
    flyer: Annotated[UploadFile, File()],
    user_id: Annotated[str, Depends(is_authenticated)],
):
    # ensure an event with title and user_id combined does not exist
    event_count = events_collection.count_documents(
        filter={"$and": [{"title": title}, {"owner": user_id}]}
    )
    if event_count > 0:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Event with{title} and {user_id} already exist",
        )
    # upload flyer to cloudinary
    upload_result = cloudinary.uploader.upload(flyer.file)
    print(upload_result)  # Debugging line to check upload result
    # insert the event into the database
    events_collection.insert_one(
        {
            "title": title,
            "description": description,
            "flyer_url": upload_result.get("secure_url"),
            "owner": user_id,
        }
    )
    # events_collection.insert_one(event.model_dump())
    return {"message": "Event added successfully"}


@events_router.get("/events/{event_id}")
def get_event_by_id(event_id):
    # check if event id is valid
    if not ObjectId.is_valid(event_id):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Invalid mongo id received",
        )
    # Get event from database by id
    event = events_collection.find_one({"_id": ObjectId(event_id)})
    # Return response
    return {"data": replace_mongo_id(event)}


@events_router.put("/events/{event_id}")
def replace_event(
    event_id,
    title: Annotated[str, Form()],
    description: Annotated[str, Form()],
    flyer: Annotated[UploadFile, File()],
):
    # check if event_id  is valid mongo id
    if not ObjectId.is_valid(event_id):
        raise HTTPException(
            status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Invalid mongo id received!"
        )
    # upload to cloudinary to the a url
    upload_result = cloudinary.uploader.upload(flyer.file)
    # Replace event in database
    events_collection.replace_one(
        filter={"_id": ObjectId(event_id)},
        replacement={
            "title": title,
            "description": description,
            "flyer_url": upload_result.get["secure_url"],
        },
    )
    # Return response
    return {"message": "Event replaced successfully"}


@events_router.delete("/events/{event_id}")
def delete_event(event_id, user_id: Annotated[str, Depends(is_authenticated)]):
    # check if event_id is valid mongo id
    if not ObjectId.is_valid(event_id):
        raise HTTPException(
            status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Invalid mongo id received"
        )
    # Delete event from database
    delete_result = events_collection.delete_one(filter={"_id": ObjectId(event_id)})
    # Return response
    if not delete_result.deleted_count:
        raise HTTPException(
            status.HTTP_422_UNPROCESSABLE_ENTITY, detail="invalid mongo id received!"
        )
    return {"message": "Event deleted successfully!"}
