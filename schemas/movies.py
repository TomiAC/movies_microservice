from pydantic import BaseModel, ConfigDict
from typing import List, Optional
from .genre import GenreRead

class MovieBase(BaseModel):
    title: str
    description: str
    year: int
    rating: Optional[float] = None
    language: str
    duration: int
    trailer: str
    image: str
    director: str

class MovieCreate(MovieBase):
    genres: List[str]

class MovieRead(MovieBase):
    id: str
    genres: List[GenreRead]
    model_config = ConfigDict(from_attributes=True)

class MovieUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    year: Optional[int] = None
    rating: Optional[float] = None
    language: Optional[str] = None
    duration: Optional[int] = None
    trailer: Optional[str] = None
    image: Optional[str] = None
    genres: Optional[List[str]] = None
    director: Optional[str] = None
    
class MovieList(BaseModel):
    movies: List[MovieRead]
    total: int
    page: int
    size: int