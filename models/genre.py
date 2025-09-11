from database import Base
from sqlalchemy import Column, Integer, String
from uuid import uuid4

class Genre(Base):
    __tablename__ = "genres"

    id = Column(String, primary_key=True, index=True, default=lambda: str(uuid4()))
    name = Column(String, unique=True)
    description = Column(String)