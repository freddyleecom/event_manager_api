from pymongo import MongoClient
import os


# connect to the Mongo Atlas cluster 
mongo_client = MongoClient(os.getenv("MONGO_URI"))

# access the database
event_manager_db = mongo_client["event_manager_db"]

# pick a collection to operate on
events_collection = event_manager_db["events"]
users_collection = event_manager_db["users"]
