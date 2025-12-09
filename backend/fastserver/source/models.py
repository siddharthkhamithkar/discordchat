import datetime
from pydantic import BaseModel


class NameRequest(BaseModel):
    name: str

class UserCreateRequest(BaseModel):
    name: str
    email_id: str
    dob: datetime.date
