from typing import Union
from dotenv import load_dotenv
from fastapi import FastAPI
from services.services import Service, get_service

app = FastAPI()
load_dotenv()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post("/services/")
async def service(request: Service):
    res = get_service(request)
    return res