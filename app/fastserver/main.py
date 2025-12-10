from fastapi import FastAPI
from contextlib import asynccontextmanager 
from api.endpoint.endpoint import app as api_router
from api.core.database import connect_to_mongo, close_mongo_connection, mongodb

@asynccontextmanager
async def lifespan(app: FastAPI):
    connect_to_mongo()
    assert mongodb.db is not None, "MongoDB connection failed"
    yield
    close_mongo_connection()

app = FastAPI(lifespan=lifespan)

app.include_router(api_router.router, prefix="/api", tags=["Backend Entities"])

@app.get("/", tags=["Health"])
def ping():
    return {"status": "ok"}