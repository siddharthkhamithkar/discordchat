from datetime import datetime, date
from pydantic import BaseModel, validator


class NameRequest(BaseModel):
    name: str

class UserCreateRequest(BaseModel):
    name: str
    email_id: str
    country_code: str
    phone_number: str

class UserCreateResponse(BaseModel):
    status: str
    name: str
    email_id: str
    country_code: str
    phone_number: str