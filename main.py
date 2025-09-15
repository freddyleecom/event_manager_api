from fastapi import FastAPI
import cloudinary
import os
from dotenv import load_dotenv
from routes.events import events_router



# Configure Cloudinary
cloudinary.config(
    cloud_name="dhqwkwo8e",
    api_key="544878511352217",
    api_secret="DB2whHclPE2tpDECsKPQNRq7G0Y"
)



app = FastAPI()

@app.get("/")
def get_home():
    return {"message": "Welcome to the Event Manager API"}  

# Include the events router
app.include_router(events_router)


