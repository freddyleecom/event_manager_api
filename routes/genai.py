from fastapi import APIRouter, Form, Depends
from typing import Annotated
from dependencies.authn import is_authenticated
from utils import genai_client


# Create a genai router
genai_router = APIRouter(tags= ["GenAI"])

# Define endpoints
@genai_router.post("genai/generate_txt", dependencies=[Depends(is_authenticated)])
def generate_text(promt = Annotated[str, Form()]):
    response = genai_client.models.generate_content(model="gemini-2.5-flash", contents=promt,)
    return{"content": response.text}