from crud.cinema import create_cinema, get_cinema, get_cinemas, update_cinema, delete_cinema
from schemas.cinema import CinemaCreate, CinemaUpdate, CinemaRead, CinemaList
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from dependencies import get_db

cinema_router = APIRouter(prefix="/cinemas", tags=["cinemas"])

@cinema_router.post("/", response_model=CinemaRead)
def create_cinema_endpoint(cinema: CinemaCreate, db: Session = Depends(get_db)):
    return create_cinema(db, cinema)

@cinema_router.get("/{cinema_id}", response_model=CinemaRead)
def get_cinema_endpoint(cinema_id: str, db: Session = Depends(get_db)):
    db_cinema = get_cinema(db, cinema_id)
    if not db_cinema:
        raise HTTPException(status_code=404, detail="Cinema not found")
    return db_cinema

@cinema_router.get("/", response_model=CinemaList)
def get_cinemas_endpoint(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return get_cinemas(db, skip, limit)

@cinema_router.put("/{cinema_id}", response_model=CinemaRead)
def update_cinema_endpoint(cinema_id: str, cinema_update: CinemaUpdate, db: Session = Depends(get_db)):
    updated_cinema = update_cinema(db, cinema_id, cinema_update)
    if not updated_cinema:
        raise HTTPException(status_code=404, detail="Cinema not found")
    return updated_cinema

@cinema_router.delete("/{cinema_id}", response_model=CinemaRead)
def delete_cinema_endpoint(cinema_id: str, db: Session = Depends(get_db)):
    deleted_cinema = delete_cinema(db, cinema_id)
    if not deleted_cinema:
        raise HTTPException(status_code=404, detail="Cinema not found")
    return deleted_cinema