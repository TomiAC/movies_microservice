from models.movie import Movie
from models.genre import Genre
from schemas.movies import MovieCreate, MovieRead, MovieUpdate, MovieList
from fastapi import HTTPException
from typing import List
from sqlalchemy.orm import Session

def create_movie(movie: MovieCreate, db: Session) -> MovieRead:
    movie_data = movie.model_dump()
    genre_ids = movie_data.pop("genres")

    db_genres = db.query(Genre).filter(Genre.id.in_(genre_ids)).all()

    if len(db_genres) != len(genre_ids):
        raise HTTPException(status_code=404, detail="One or more genres not found")

    new_movie = Movie(**movie_data)
    new_movie.genres = db_genres
    
    db.add(new_movie)
    db.commit()
    db.refresh(new_movie)
    return MovieRead.model_validate(new_movie)

def get_movie(movie_id: str, db: Session) -> MovieRead:
    movie = db.query(Movie).filter(Movie.id == movie_id).first()
    if not movie:
        return None
    return MovieRead.model_validate(movie)

def get_movie_by_title(title: str, db: Session) -> MovieRead:
    movie = db.query(Movie).filter(Movie.title == title).first()
    if not movie:
        return None
    return MovieRead.model_validate(movie)

def get_movies(db: Session, page: int = 1, size: int = 10) -> MovieList:
    skip = (page - 1) * size
    total = db.query(Movie).count()
    movies = db.query(Movie).offset(skip).limit(size).all()
    return MovieList(
        movies=[MovieRead.model_validate(movie) for movie in movies],
        total=total,
        page=page,
        size=size
    )

def update_movie(movie_id: str, movie: MovieUpdate, db: Session) -> MovieRead:
    existing_movie = db.query(Movie).filter(Movie.id == movie_id).first()
    if not existing_movie:
        return None
    
    update_data = movie.model_dump(exclude_unset=True)
    
    if "genres" in update_data:
        genre_names = update_data.pop("genres")
        db_genres = db.query(Genre).filter(Genre.name.in_(genre_names)).all()
        if len(db_genres) != len(genre_names):
            raise HTTPException(status_code=404, detail="One or more genres not found")
        existing_movie.genres = db_genres

    for key, value in update_data.items():
        setattr(existing_movie, key, value)
        
    db.commit()
    db.refresh(existing_movie)
    return MovieRead.model_validate(existing_movie)

def delete_movie(movie_id: str, db: Session) -> MovieRead:
    movie = db.query(Movie).filter(Movie.id == movie_id).first()
    if not movie:
        return None
    db.delete(movie)
    db.commit()
    return MovieRead.model_validate(movie)