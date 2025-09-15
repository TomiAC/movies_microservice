from models.auditorium import Auditorium
from schemas.auditorium import AuditoriumCreate, AuditoriumRead, AuditoriumUpdate
from sqlalchemy.orm import Session
from typing import List, Optional

def create_auditorium(db: Session, auditorium: AuditoriumCreate) -> AuditoriumRead:
    db_auditorium = Auditorium(**auditorium.model_dump())
    db.add(db_auditorium)
    db.commit()
    db.refresh(db_auditorium)
    return AuditoriumRead.model_validate(db_auditorium)

def get_auditorium(db: Session, auditorium_id: str) -> AuditoriumRead | None:
    db_auditorium = db.query(Auditorium).filter(Auditorium.id == auditorium_id).first()
    if db_auditorium:
        return AuditoriumRead.model_validate(db_auditorium)
    return None

def get_auditoriums(db: Session, skip: int = 0, limit: int = 100) -> List[AuditoriumRead]:
    db_auditoriums = db.query(Auditorium).offset(skip).limit(limit).all()
    auditoriums = [AuditoriumRead.model_validate(auditorium) for auditorium in db_auditoriums]
    page = (skip // limit) + 1 if limit > 0 else 1
    return {
        "auditoriums": auditoriums,
        "total": len(auditoriums),
        "page": page,
        "size": limit,
    }

def update_auditorium(db: Session, auditorium_id: str, auditorium_update: AuditoriumUpdate) -> AuditoriumRead | None:
    db_auditorium = db.query(Auditorium).filter(Auditorium.id == auditorium_id).first()
    if not db_auditorium:
        return None
    update_data = auditorium_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_auditorium, key, value)
    db.commit()
    db.refresh(db_auditorium)
    return AuditoriumRead.model_validate(db_auditorium)

def delete_auditorium(db: Session, auditorium_id: str) -> AuditoriumRead | None:
    db_auditorium = db.query(Auditorium).filter(Auditorium.id == auditorium_id).first()
    if not db_auditorium:
        return None
    db.delete(db_auditorium)
    db.commit()
    return AuditoriumRead.model_validate(db_auditorium)
