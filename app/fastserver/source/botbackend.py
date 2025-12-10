from fastapi import FastAPI
from app.fastserver.api.models.models import NameRequest, UserCreateRequest, UserCreateResponse
app = FastAPI()


@app.post("/echo")
def echo_name(payload: NameRequest):
    return {"name": payload.name}


@app.post("/create_user/", response_model=str, dependencies=[Depends(verify_token)])
async def add_entity(payload: CustomerCreate):
    try:
        entity_id = await create_entity(payload.dict())
        return entity_id
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")