from fastapi import FastAPI
from models import NameRequest, UserCreateRequest, UserCreateResponse
app = FastAPI()


@app.post("/echo")
def echo_name(payload: NameRequest):
    return {"name": payload.name}

@app.post("/createUser", response_model=UserCreateResponse)
def create_user(payload: UserCreateRequest):
    # Placeholder implementation
    print(payload)
    return UserCreateResponse(
        status="User created",
        name=payload.name,
        email_id=payload.email_id,
        country_code=payload.country_code,
        phone_number=payload.phone_number,
    )a