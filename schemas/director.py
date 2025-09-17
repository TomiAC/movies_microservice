from pydantic import BaseModel, ConfigDict
from typing import List, Optional
from datetime import date

class DirectorBase(BaseModel):
    name: str
    birth_date: Optional[date] = None
    nationality: Optional[str] = None
    bio: Optional[str] = None

class DirectorCreate(DirectorBase):
    pass

class DirectorRead(DirectorBase):
    id: str
    model_config = ConfigDict(from_attributes=True)

class DirectorUpdate(BaseModel):
    name: Optional[str] = None
    birth_date: Optional[date] = None
    nationality: Optional[str] = None
    bio: Optional[str] = None

class DirectorList(BaseModel):
    directors: List[DirectorRead]
    total: int
    page: int
    size: int
