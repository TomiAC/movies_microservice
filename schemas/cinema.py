from pydantic import BaseModel, ConfigDict
from typing import List

class CinemaBase(BaseModel):
    name: str
    location: str
    number: int

class CinemaCreate(CinemaBase):
    pass

class CinemaRead(CinemaBase):
    id: str
    model_config = ConfigDict(from_attributes=True)

class CinemaUpdate(BaseModel):
    name: str | None = None
    location: str | None = None
    number: int | None = None

class CinemaList(BaseModel):
    cinemas: List[CinemaRead]
    total: int
    page: int
    size: int