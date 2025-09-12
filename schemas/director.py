from pydantic import BaseModel
from typing import List, Optional

class DirectorCreate(BaseModel):
    name: str
    birth_date: Optional[str] = None
    nationality: Optional[str] = None
    bio: Optional[str] = None

class DirectorRead(DirectorCreate):
    id: str
    name: str
    birth_date: Optional[str] = None
    nationality: Optional[str] = None
    bio: Optional[str] = None

class DirectorUpdate(BaseModel):
    name: Optional[str] = None
    birth_date: Optional[str] = None
    nationality: Optional[str] = None
    bio: Optional[str] = None

class DirectorList(BaseModel):
    directors: List[DirectorRead]
    total: int
    page: int
    size: int