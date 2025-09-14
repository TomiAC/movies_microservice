from schemas.cinema import CinemaCreate, CinemaUpdate, CinemaRead
from models.cinema import Cinema
from sqlalchemy.orm import Session
from typing import List

def create_cinema(db: Session, cinema: CinemaCreate) -> CinemaRead:
    db_cinema = Cinema(**cinema.model_dump())
    db.add(db_cinema)
    db.commit()
    db.refresh(db_cinema)
    return CinemaRead.model_validate(db_cinema)

def get_cinema(db: Session, cinema_id: str) -> CinemaRead:
    db_cinema = db.query(Cinema).filter(Cinema.id == cinema_id).first()
    if not db_cinema:
        return None
    return CinemaRead.model_validate(db_cinema)

def get_cinemas(db: Session, skip: int = 0, limit: int = 100) -> dict:
    total = db.query(Cinema).count()
    db_cinemas = db.query(Cinema).offset(skip).limit(limit).all()
    cinemas = [CinemaRead.model_validate(cinema) for cinema in db_cinemas]
    page = (skip // limit) + 1 if limit > 0 else 1
    return {
        "cinemas": cinemas,
        "total": total,
        "page": page,
        "size": limit,
    }

def update_cinema(db: Session, cinema_id: str, cinema_update: CinemaUpdate) -> CinemaRead:
    db_cinema = db.query(Cinema).filter(Cinema.id == cinema_id).first()
    if not db_cinema:
        return None
    update_data = cinema_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_cinema, key, value)
    db.commit()
    db.refresh(db_cinema)
    return CinemaRead.model_validate(db_cinema)

def delete_cinema(db: Session, cinema_id: str) -> CinemaRead:
    db_cinema = db.query(Cinema).filter(Cinema.id == cinema_id).first()
    if not db_cinema:
        return None
    db.delete(db_cinema)
    db.commit()
    return CinemaRead.model_validate(db_cinema)