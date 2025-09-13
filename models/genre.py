from database import Base
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from sqlalchemy.ext.associationproxy import association_proxy
from uuid import uuid4

class Genre(Base):
    __tablename__ = "genres"

    id = Column(String, primary_key=True, index=True, default=lambda: str(uuid4()))
    name = Column(String, unique=True)
    description = Column(String)

    movies_association = relationship("MovieGenre", back_populates="genre", cascade="all, delete-orphan")
    movies = association_proxy("movies_association", "movie")