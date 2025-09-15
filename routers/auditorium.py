from fastapi import APIRouter, Depends, HTTPException
from schemas.auditorium import AuditoriumCreate, AuditoriumRead, AuditoriumUpdate, AuditoriumList
from crud.auditorium import create_auditorium, get_auditorium, get_auditoriums, update_auditorium, delete_auditorium
from crud.cinema import get_cinema
from database import get_db
from sqlalchemy.orm import Session

auditorium_router = APIRouter(prefix="/auditoriums", tags=["auditoriums"])

@auditorium_router.post("/", response_model=AuditoriumRead)
def create_auditorium_endpoint(auditorium: AuditoriumCreate, db: Session = Depends(get_db)):
    cinema = get_cinema(db, auditorium.cinema_id)
    if not cinema:
        raise HTTPException(status_code=400, detail="Cinema does not exist")
    new_auditorium = create_auditorium(db, auditorium)
    if not new_auditorium:
        raise HTTPException(status_code=400, detail="Failed to create auditorium")
    return new_auditorium

@auditorium_router.get("/{auditorium_id}", response_model=AuditoriumRead)
def get_auditorium_endpoint(auditorium_id: str, db: Session = Depends(get_db)):
    auditorium = get_auditorium(db, auditorium_id)
    if not auditorium:
        raise HTTPException(status_code=404, detail="Auditorium not found")
    return auditorium

@auditorium_router.get("/", response_model=AuditoriumList)
def get_auditoriums_endpoint(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    auditoriums_data = get_auditoriums(db, skip=skip, limit=limit)
    return AuditoriumList(**auditoriums_data)

@auditorium_router.put("/{auditorium_id}", response_model=AuditoriumRead)
def update_auditorium_endpoint(auditorium_id: str, auditorium_update: AuditoriumUpdate, db: Session = Depends(get_db)):
    updated_auditorium = update_auditorium(db, auditorium_id, auditorium_update)
    if not updated_auditorium:
        raise HTTPException(status_code=404, detail="Auditorium not found")
    return updated_auditorium

@auditorium_router.delete("/{auditorium_id}", response_model=AuditoriumRead)
def delete_auditorium_endpoint(auditorium_id: str, db: Session = Depends(get_db)):
    deleted_auditorium = delete_auditorium(db, auditorium_id)
    if not deleted_auditorium:
        raise HTTPException(status_code=404, detail="Auditorium not found")
    return deleted_auditorium
