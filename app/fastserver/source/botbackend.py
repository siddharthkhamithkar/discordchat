from fastapi import FastAPI
from models import UserCreateRequest, UserCreateResponse
app = FastAPI()


@app.post("/echo")
def echo_name(payload: UserCreateRequest):
    return {"name": payload.name}

