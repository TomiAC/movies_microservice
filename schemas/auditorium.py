from pydantic import BaseModel, ConfigDict
from typing import Optional

class Auditorium(BaseModel):
    name: str
    cinema_id: str
    capacity: int

class AuditoriumCreate(Auditorium):
    pass

class AuditoriumRead(Auditorium):
    id: str
    model_config = ConfigDict(from_attributes=True)

class AuditoriumUpdate(BaseModel):
    name: Optional[str] = None
    cinema_id: Optional[str] = None
    capacity: Optional[int] = None

class AuditoriumList(BaseModel):
    auditoriums: list[AuditoriumRead]
    total: int
    page: int
    size: int
