from fastapi import FastAPI, HTTPException
from api.models.models import UserCreateRequest
from api.services.services import create_user


app = FastAPI()


@app.post("/create_user/", response_model=str)
async def create_user_endpoint(payload: UserCreateRequest):
    try:
        entity_id = await create_user(payload)
        return entity_id
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")