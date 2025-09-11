from database import Base
from sqlalchemy import Column, Integer, String, ForeignKey
from uuid import uuid4

class Cinema(Base):
    __tablename__ = 'cinemas'

    id = Column(String, primary_key=True, default=lambda: str(uuid4()))
    name = Column(String, nullable=False)
    location = Column(String, nullable=False)
    number = Column(Integer, nullable=False)


    def __repr__(self):
        return f"<Cinema(id={self.id}, name={self.name}, location={self.location}, number={self.number})>"