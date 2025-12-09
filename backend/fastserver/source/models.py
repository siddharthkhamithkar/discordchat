from datetime import datetime, date
from pydantic import BaseModel, validator


class NameRequest(BaseModel):
    name: str

class UserCreateRequest(BaseModel):
    name: str
    email_id: str
    @validator("dob", pre=True)
    def parse_dob(cls, value):
        # Convert "dd/mm/yyyy" -> date object
        return datetime.strptime(value, "%d/%m/%Y").date()
