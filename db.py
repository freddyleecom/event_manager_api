from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

# connect to the Mongo Atlas cluster 
mongo_client = MongoClient(os.getenv("MONGO_URL"))

# access the database
event_manager_db = mongo_client["event_manager_db"]

# pick a collection to operate on
events_collection = event_manager_db["events"]
