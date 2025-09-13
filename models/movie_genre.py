from database import Base
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship

class MovieGenre(Base):
    __tablename__ = 'movie_genre'
    movie_id = Column(String, ForeignKey('movies.id'), primary_key=True)
    genre_id = Column(String, ForeignKey('genres.id'), primary_key=True)

    movie = relationship("Movie", back_populates="genres_association")
    genre = relationship("Genre", back_populates="movies_association")

    def __init__(self, value=None):
        if value is not None:
            if hasattr(value, 'title'):
                self.movie = value
            elif hasattr(value, 'name'):
                self.genre = value