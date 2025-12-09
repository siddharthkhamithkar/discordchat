from datetime import datetime, date
from pydantic import BaseModel, validator


class NameRequest(BaseModel):
    name: str

class UserCreateRequest(BaseModel):
    name: str
    email_id: str
    dob: date
    @validator("dob", pre=True)
    def parse_dob(cls, v):
        # User inputs dd/mm/yyyy
        return datetime.strptime(v, "%d/%m/%Y").date()

class UserCreateResponse(BaseModel):
    status: str
    name: str
    email_id: str
    dob: date