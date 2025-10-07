from fastapi import APIRouter, HTTPException, Depends
from typing import List
from schemas.movies import MovieCreate, MovieRead, MovieUpdate, MovieList
from schemas.user import UserRole
from dependencies import get_db, RoleRequired
from sqlalchemy.ext.asyncio import AsyncSession
from crud.movies import create_movie as create_movie_crud, get_movie, get_movies, update_movie, delete_movie, get_movie_by_title, get_list_of_movies_by_title_like, get_movies_by_genre
from crud.director import get_director
from crud.genre import get_genre

movie_router = APIRouter(prefix="/movies", tags=["movies"])

@movie_router.post("/", response_model=MovieRead)
async def create_movie(movie: MovieCreate, db: AsyncSession = Depends(get_db), role: UserRole = Depends(RoleRequired([UserRole.ADMIN, UserRole.STAFF]))):
    director = await get_director(movie.director, db)
    print(director)
    if not director:
        raise HTTPException(status_code=400, detail="Director not found")
    for genre_id in movie.genres:
        genre = await get_genre(genre_id, db)
        print(genre)
        if not genre:
            raise HTTPException(status_code=400, detail="Genre not found")
    return await create_movie_crud(movie, db)

@movie_router.get("/{movie_id}", response_model=MovieRead)
async def get_movie_endpoint(movie_id: str, db: AsyncSession = Depends(get_db)):
    searched_movie = await get_movie(movie_id, db)
    if not searched_movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    return searched_movie

@movie_router.get("/title/{title}", response_model=MovieRead)
async def get_movie_by_title_endpoint(title: str, db: AsyncSession = Depends(get_db)):
    searched_movie = await get_movie_by_title(title, db)
    if not searched_movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    return searched_movie

@movie_router.get("/title_like/{name}", response_model=List[MovieRead])
async def get_list_of_movies_by_title_like_endpoint(name: str, db: AsyncSession = Depends(get_db)):
    return await get_list_of_movies_by_title_like(name, db)

@movie_router.get("/genre/{genre_id}", response_model=List[MovieRead])
async def get_movies_by_genre_endpoint(genre_id: str, db: AsyncSession = Depends(get_db)):
    genre = await get_genre(genre_id, db)
    if not genre:
        raise HTTPException(status_code=404, detail="Genre not found")
    return await get_movies_by_genre(genre_id, db)

@movie_router.get("/", response_model=MovieList)
async def get_movies_endpoint(page: int = 1, size: int = 10, db: AsyncSession = Depends(get_db)):
    return await get_movies(db, page, size)

@movie_router.put("/{movie_id}", response_model=MovieRead)
async def update_movie_endpoint(movie_id: str, movie: MovieUpdate, db: AsyncSession = Depends(get_db), role: UserRole = Depends(RoleRequired([UserRole.ADMIN, UserRole.STAFF]))):
    existing_movie = await get_movie(movie_id, db)
    if not existing_movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    updated_movie = await update_movie(movie_id, movie, db)
    return updated_movie

@movie_router.delete("/{movie_id}", response_model=MovieRead)
async def delete_movie_endpoint(movie_id: str, db: AsyncSession = Depends(get_db), role: UserRole = Depends(RoleRequired([UserRole.ADMIN, UserRole.STAFF]))):
    movie = await get_movie(movie_id, db)
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    await delete_movie(movie_id, db)
    return movie