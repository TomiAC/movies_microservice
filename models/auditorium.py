from database import Base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from uuid import uuid4

class Auditorium(Base):
    __tablename__ = 'auditoriums'

    id = Column(String, primary_key=True, default=lambda: str(uuid4()))
    name = Column(String, nullable=False)
    cinema_id = Column(String, ForeignKey('cinemas.id'), nullable=False)
    capacity = Column(Integer, nullable=False)

    cinema = relationship("Cinema", backref="auditoriums")

    def __repr__(self):
        return f"<Auditorium(id={self.id}, name={self.name}, cinema_id={self.cinema_id}, capacity={self.capacity})>"