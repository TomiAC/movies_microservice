from pydantic import BaseModel, ConfigDict
from typing import List, Optional

class GenreBase(BaseModel):
    name: str
    description: Optional[str] = None

class GenreCreate(GenreBase):
    pass

class GenreRead(GenreCreate):
    id: str
    model_config = ConfigDict(from_attributes=True)

class GenreUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None

class GenreList(BaseModel):
    genres: List[GenreRead]
    total: int
    page: int
    size: int