from crud.genre import create_genre, get_genre, get_genres, update_genre, delete_genre
from fastapi import APIRouter, HTTPException, Depends
from typing import List
from schemas.genre import GenreCreate, GenreRead, GenreUpdate, GenreList
from dependencies import get_db
from sqlalchemy.orm import Session

genre_router = APIRouter(prefix="/genres", tags=["genres"])

@genre_router.post("/", response_model=GenreRead)
async def create_genre_endpoint(genre: GenreCreate, db: Session = Depends(get_db)):
    new_genre = create_genre(genre, db)
    if not new_genre:
        raise HTTPException(status_code=400, detail="Genre could not be created")
    return new_genre

@genre_router.get("/{genre_id}", response_model=GenreRead)
async def get_genre_endpoint(genre_id: str, db: Session = Depends(get_db)):
    genre = get_genre(genre_id, db)
    if not genre:
        raise HTTPException(status_code=404, detail="Genre not found")
    return genre

@genre_router.get("/", response_model=GenreList)
async def get_genres_endpoint(page: int = 1, size: int = 10, db: Session = Depends(get_db)):
    return get_genres(db, page, size)

@genre_router.put("/{genre_id}", response_model=GenreRead)
async def update_genre_endpoint(genre_id: str, genre: GenreUpdate, db: Session = Depends(get_db)):
    updated_genre = update_genre(genre_id, genre, db)
    if not updated_genre:
        raise HTTPException(status_code=404, detail="Genre not found")
    return updated_genre

@genre_router.delete("/{genre_id}", response_model=GenreRead)
async def delete_genre_endpoint(genre_id: str, db: Session = Depends(get_db)):
    deleted_genre = delete_genre(genre_id, db)
    if not deleted_genre:
        raise HTTPException(status_code=404, detail="Genre not found")
    return deleted_genre