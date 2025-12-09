from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class NameRequest(BaseModel):
    name: str

@app.post("/echo")
def echo_name(payload: NameRequest):
    return {"name": payload.name}