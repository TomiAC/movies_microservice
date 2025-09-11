from database import Base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from uuid import uuid4

class Movie(Base):
    __tablename__ = "movies"

    id = Column(String, primary_key=True, index=True, default=lambda: str(uuid4()))
    name = Column(String)
    year = Column(Integer)
    rating = Column(Integer)
    description = Column(String)
    image = Column(String)
    trailer = Column(String)
    duration = Column(Integer)
    language = Column(String)
    genre = Column(String, ForeignKey("genres.id"), nullable=False)
    director = Column(String, ForeignKey("directors.id"), nullable=False)

    genre_rel = relationship("Genre", back_populates="movies")
    director_rel = relationship("Director", back_populates="movies")