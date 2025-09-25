from pydantic import BaseModel
from enum import Enum

class UserRole(str, Enum):
    USER = "user"
    STAFF = "staff"
    ADMIN = "admin"

class TokenData(BaseModel):
    id: str
    role: UserRole