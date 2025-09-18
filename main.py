from fastapi import FastAPI
import cloudinary
from routes.events import events_router
from routes.users import users_router
import os
from dotenv import load_dotenv

load_dotenv



# Configure Cloudinary
cloudinary.config(
    cloud_name=os.getenv("dhqwkwo8e"),
    api_key=os.getenv("544878511352217"),
    api_secret=os.getenv("DB2whHclPE2tpDECsKPQNRq7G0Y")
)



app = FastAPI()

@app.get("/")
def get_home():
    return {"message": "Welcome to the Event Manager API"}  

# Include the events router
app.include_router(events_router)
app.include_router(users_router)



