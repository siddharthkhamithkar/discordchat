from datetime import datetime, date
from pydantic import BaseModel, validator


class NameRequest(BaseModel):
    name: str

class UserCreateRequest(BaseModel):
    name: str
    email_id: str
    @validator("dob", pre=True)
    def parse_dob(cls, v):
        # User inputs dd/mm/yyyy
        return datetime.strptime(v, "%d/%m/%Y").date()
