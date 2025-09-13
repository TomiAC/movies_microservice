from fastapi import APIRouter, HTTPException, Depends
from typing import List
from schemas.movies import MovieCreate, MovieRead, MovieUpdate, MovieList
from dependencies import get_db
from sqlalchemy.orm import Session
from crud.movies import create_movie as create_movie_crud, get_movie, get_movies, update_movie, delete_movie
from crud.director import get_director
from crud.genre import get_genre

movie_router = APIRouter(prefix="/movies", tags=["movies"])

@movie_router.post("/", response_model=MovieRead)
async def create_movie(movie: MovieCreate, db: Session = Depends(get_db)):
    director = get_director(movie.director, db)
    if not director:
        raise HTTPException(status_code=400, detail="Director not found")
    for genre_id in movie.genres:
        genre = get_genre(genre_id, db)
        if not genre:
            raise HTTPException(status_code=400, detail="Genre not found")
    return create_movie_crud(movie, db)

@movie_router.get("/{movie_id}", response_model=MovieRead)
async def get_movie(movie_id: str, db: Session = Depends(get_db)):
    searched_movie = await get_movie(movie_id, db)
    if not searched_movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    return MovieRead(**searched_movie.model_dump())

@movie_router.get("/", response_model=MovieList)
async def get_movies(page: int = 1, size: int = 10, db: Session = Depends(get_db)):
    return get_movies(page, size, db)

@movie_router.put("/{movie_id}", response_model=MovieRead)
async def update_movie(movie_id: str, movie: MovieUpdate, db: Session = Depends(get_db)):
    existing_movie = await get_movie(movie_id, db)
    if not existing_movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    updated_movie = await update_movie(movie_id, movie, db)
    return MovieRead(**updated_movie.model_dump())

@movie_router.delete("/{movie_id}", response_model=MovieRead)
async def delete_movie(movie_id: str, db: Session = Depends(get_db)):
    movie = await get_movie(movie_id, db)
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    await delete_movie(movie_id, db)
    return MovieRead(**movie.model_dump())
