from models.director import Director
from schemas.director import DirectorCreate, DirectorRead, DirectorUpdate, DirectorList
from typing import List
from sqlalchemy.orm import Session

def create_director(director: DirectorCreate, db: Session) -> DirectorRead:
    new_director = Director(**director.model_dump())
    db.add(new_director)
    db.commit()
    db.refresh(new_director)
    return DirectorRead(**new_director.model_dump())

def get_director(director_id: str, db: Session) -> DirectorRead:
    director = db.query(Director).filter(Director.id == director_id).first()
    if not director:
        return None
    return DirectorRead(**director.model_dump())

def get_directors(db: Session, page: int = 1, size: int = 10) -> DirectorList:
    skip = (page - 1) * size
    total = db.query(Director).count()
    directors = db.query(Director).offset(skip).limit(size).all()
    return DirectorList(
        directors=[DirectorRead(**director.model_dump()) for director in directors],
        total=total,
        page=page,
        size=size
    )

def update_director(director_id: str, director: DirectorUpdate, db: Session) -> DirectorRead:
    existing_director = db.query(Director).filter(Director.id == director_id).first()
    if not existing_director:
        return None
    updated_director = existing_director.copy(update=director.model_dump())
    db.commit()
    db.refresh(updated_director)
    return DirectorRead(**updated_director.model_dump())

def delete_director(director_id: str, db: Session) -> DirectorRead:
    director = db.query(Director).filter(Director.id == director_id).first()
    if not director:
        return None
    db.delete(director)
    db.commit()
    return DirectorRead(**director.model_dump())