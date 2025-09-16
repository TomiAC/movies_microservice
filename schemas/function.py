from pydantic import BaseModel, ConfigDict
from typing import List, Optional
from datetime import datetime, date

class FunctionBase(BaseModel):
    start_time: datetime
    end_time: datetime
    price: float
    available_seats: int
    movie_id: str
    auditorium_id: str

class FunctionCreate(FunctionBase):
    pass

class FunctionRead(FunctionBase):
    id: str
    model_config = ConfigDict(from_attributes=True)

class FunctionUpdate(BaseModel):
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    price: Optional[float] = None
    available_seats: Optional[int] = None
    movie_id: Optional[str] = None
    auditorium_id: Optional[str] = None

class FunctionList(BaseModel):
    functions: List[FunctionRead]
    total: int
    page: int
    size: int