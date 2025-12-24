from fastapi import FastAPI, HTTPException
from api.models.models import UserCreateRequest
from api.services.services import create_user, validate_user


app = FastAPI()


@app.post("/create_user/", response_model=str)
async def create_user_endpoint(payload: UserCreateRequest):
    try:
        entity_id = await create_user(payload)
        return entity_id
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")
    
@app.post("/validate_user/", response_model=bool)
async def validate_user_endpoint(email_id: str):
    try:
        is_valid = await validate_user(email_id)
        return is_valid
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")