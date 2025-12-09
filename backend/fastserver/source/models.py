from datetime import datetime, date
from pydantic import BaseModel, field_validator


class NameRequest(BaseModel):
    name: str

class UserCreateRequest(BaseModel):
    name: str
    email_id: str
    @field_validator("dob", mode="before")
    def parse_dob(cls, v):
        return datetime.strptime(v, "%d/%m/%Y").date()
