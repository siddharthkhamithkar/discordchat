from fastapi import FastAPI
from models import NameRequest, UserCreateRequest
app = FastAPI()


@app.post("/echo")
def echo_name(payload: NameRequest):
    return {"name": payload.name}

@app.post("/createUser")
def create_user(payload: UserCreateRequest):
    # Placeholder implementation
    print(payload)
    return {"status": "User created", "name": payload.name, "email_id": payload.email_id, "dob": str(payload.dob)}