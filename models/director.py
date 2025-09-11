from database import Base
from sqlalchemy import Column, Integer, String
from uuid import uuid4

class Director(Base):
    __tablename__ = "directors"

    id = Column(String, primary_key=True, index=True, default=lambda: str(uuid4()))
    name = Column(String, unique=True)
    bio = Column(String)
    birth_date = Column(String)
    nationality = Column(String)
    image = Column(String)