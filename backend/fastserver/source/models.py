from datetime import datetime, date
from pydantic import BaseModel, validator


class NameRequest(BaseModel):
    name: str

class UserCreateRequest(BaseModel):
    name: str
    email_id: str

class UserCreateResponse(BaseModel):
    status: str
    name: str
    email_id: str