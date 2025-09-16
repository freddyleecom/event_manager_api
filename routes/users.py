from fastapi import APIRouter, Form, HTTPException,status
from typing import Annotated
from pydantic import EmailStr
from db import users_collection
import bcrypt

# Create users router
users_router = APIRouter()

# define endpoints here
@users_router.post("/users/register")
def register_user(
    username: Annotated[str,Form()],
    email: Annotated[EmailStr, Form()],
    password: Annotated[str, Form(min_length=8)]):
    # Ensure user does not exist
    user_count = users_collection.count_documents(filter={"email":email})
    if user_count > 0:
       raise HTTPException(status.HTTP_409_CONFLICT, "user already exist!")
    
    # hash your password
    hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())

    # save user into database
    users_collection.insert_one({
        "username":username,
        "email": email,
        "password": hashed_password
    })
    # Return response
    return {"message": "User registered successfully"}