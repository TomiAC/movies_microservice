from database import Base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.associationproxy import association_proxy
from uuid import uuid4

class Movie(Base):
    __tablename__ = "movies"

    id = Column(String, primary_key=True, index=True, default=lambda: str(uuid4()))
    title = Column(String)
    year = Column(Integer)
    rating = Column(Integer)
    description = Column(String)
    image = Column(String)
    trailer = Column(String)
    duration = Column(Integer)
    language = Column(String)
    director = Column(String, ForeignKey("directors.id"), nullable=False)

    genres_association = relationship("MovieGenre", back_populates="movie", cascade="all, delete-orphan")
    genres = association_proxy("genres_association", "genre")
    
    director_rel = relationship("Director", back_populates="movies")