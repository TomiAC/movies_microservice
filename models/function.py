from database import Base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from uuid import uuid4

class Function(Base):
    __tablename__ = 'functions'

    id = Column(String, primary_key=True, default=lambda: str(uuid4()))
    movie_id = Column(String, ForeignKey('movies.id'), nullable=False)
    auditorium_id = Column(String, ForeignKey('auditoriums.id'), nullable=False)
    start_time = Column(String, nullable=False)
    end_time = Column(String, nullable=False)
    date = Column(String, nullable=False)
    price = Column(Integer, nullable=False)
    available_seats = Column(Integer, nullable=False)

    movie = relationship("Movie", backref="functions")
    auditorium = relationship("Auditorium", backref="functions")

    def __repr__(self):
        return f"<Function(id={self.id}, movie_id={self.movie_id}, auditorium_id={self.auditorium_id}, start_time={self.start_time}, end_time={self.end_time}, date={self.date}, price={self.price})>"
