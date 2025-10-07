from models.movie import Movie
from models.genre import Genre
from models.movie_genre import MovieGenre
from schemas.movies import MovieCreate, MovieRead, MovieUpdate, MovieList
from fastapi import HTTPException
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy import func


async def create_movie(movie: MovieCreate, db: AsyncSession) -> MovieRead:
    print("Creating movie:", movie)
    movie_data = movie.model_dump()
    genre_ids = movie_data.pop("genres")

    result = await db.execute(select(Genre).where(Genre.id.in_(genre_ids)))
    db_genres = result.scalars().all()

    if len(db_genres) != len(genre_ids):
        raise HTTPException(status_code=404, detail="One or more genres not found")

    new_movie = Movie(**movie_data)
    new_movie.genres = db_genres
    
    db.add(new_movie)
    await db.commit()
    await db.refresh(new_movie)
    
    result = await db.execute(select(Movie).where(Movie.id == new_movie.id).options(selectinload(Movie.genres_association).selectinload(MovieGenre.genre)))
    created_movie = result.scalars().first()
    
    return MovieRead.model_validate(created_movie)

async def get_movie(movie_id: str, db: AsyncSession) -> MovieRead:
    result = await db.execute(select(Movie).where(Movie.id == movie_id).options(selectinload(Movie.genres_association).selectinload(MovieGenre.genre)))
    movie = result.scalars().first()
    if not movie:
        return None
    return MovieRead.model_validate(movie)

async def get_movie_by_title(title: str, db: AsyncSession) -> MovieRead:
    result = await db.execute(select(Movie).where(Movie.title == title).options(selectinload(Movie.genres_association).selectinload(MovieGenre.genre)))
    movie = result.scalars().first()
    if not movie:
        return None
    return MovieRead.model_validate(movie)

async def get_list_of_movies_by_title_like(name: str, db: AsyncSession):
    result = await db.execute(select(Movie).where(Movie.title.like(f"%{name}%")).options(selectinload(Movie.genres_association).selectinload(MovieGenre.genre)))
    movies_query = result.scalars().all()
    return [MovieRead.model_validate(movie) for movie in movies_query]

async def get_movies_by_genre(genre_id: str, db: AsyncSession) -> List[MovieRead]:
    result = await db.execute(select(Movie).where(Movie.genres.any(id=genre_id)).options(selectinload(Movie.genres_association).selectinload(MovieGenre.genre)))
    movies = result.scalars().all()
    return [MovieRead.model_validate(movie) for movie in movies]

async def get_movies(db: AsyncSession, page: int = 1, size: int = 10) -> MovieList:
    skip = (page - 1) * size
    total_result = await db.execute(select(func.count(Movie.id)))
    total = total_result.scalar()
    
    result = await db.execute(select(Movie).offset(skip).limit(size).options(selectinload(Movie.genres_association).selectinload(MovieGenre.genre)))
    movies = result.scalars().all()
    
    return MovieList(
        movies=[MovieRead.model_validate(movie) for movie in movies],
        total=total,
        page=page,
        size=size
    )

async def update_movie(movie_id: str, movie: MovieUpdate, db: AsyncSession) -> MovieRead:
    result = await db.execute(select(Movie).where(Movie.id == movie_id).options(selectinload(Movie.genres_association).selectinload(MovieGenre.genre)))
    existing_movie = result.scalars().first()

    if not existing_movie:
        return None
    
    update_data = movie.model_dump(exclude_unset=True)
    
    if "genres" in update_data:
        genre_ids = update_data.pop("genres")
        result = await db.execute(select(Genre).where(Genre.id.in_(genre_ids)))
        db_genres = result.scalars().all()
        if len(db_genres) != len(genre_ids):
            raise HTTPException(status_code=404, detail="One or more genres not found")
        existing_movie.genres = db_genres

    for key, value in update_data.items():
        setattr(existing_movie, key, value)
        
    await db.commit()
    await db.refresh(existing_movie)
    
    result = await db.execute(select(Movie).where(Movie.id == existing_movie.id).options(selectinload(Movie.genres_association).selectinload(MovieGenre.genre)))
    updated_movie = result.scalars().first()
    
    return MovieRead.model_validate(updated_movie)

async def delete_movie(movie_id: str, db: AsyncSession) -> MovieRead:
    result = await db.execute(select(Movie).where(Movie.id == movie_id).options(selectinload(Movie.genres_association).selectinload(MovieGenre.genre)))
    movie = result.scalars().first()
    if not movie:
        return None
    await db.delete(movie)
    await db.commit()
    return MovieRead.model_validate(movie)