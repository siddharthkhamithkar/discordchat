from datetime import datetime
from fastapi import HTTPException
from pymongo.errors import DuplicateKeyError
from typing import Optional
from api.utils.utils import get_user_collection
from api.models.models import UserCreateRequest

async def create_user(user_data: UserCreateRequest) -> str:
    collection = get_user_collection()
    
    # Check if email already exists
    if collection.find_one({"email": user_data.email_id}):
        raise HTTPException(status_code=400, detail="Email already exists")
    
    # Check if phone already exists
    if collection.find_one({"phone": user_data.phone_number}):
        raise HTTPException(status_code=400, detail="Phone already exists")
    
    # Prepare user document
    user_doc = {
        "name": user_data.name,
        "email": user_data.email_id,
        "countrycode": user_data.country_code,
        "phone": user_data.phone_number,
        "created_at": datetime.now(),
    }
    
    try:
        # Insert the user
        result = collection.insert_one(user_doc)
        return str(result.inserted_id)
    except DuplicateKeyError:
        raise HTTPException(status_code=400, detail="User with this email or phone already exists")