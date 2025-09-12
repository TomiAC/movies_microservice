from models.director import Director
from schemas.director import DirectorCreate, DirectorRead, DirectorUpdate, DirectorList
from typing import List
from sqlalchemy.orm import Session

def create_director(director: DirectorCreate, db: Session) -> DirectorRead:
    new_director = Director(**director.model_dump())
    db.add(new_director)
    db.commit()
    db.refresh(new_director)
    return DirectorRead.model_validate(new_director)

def get_director(director_id: str, db: Session) -> DirectorRead | None:
    director = db.query(Director).filter(Director.id == director_id).first()
    if not director:
        return None
    return DirectorRead.model_validate(director)

def get_directors(db: Session, page: int = 1, size: int = 10) -> DirectorList:
    skip = (page - 1) * size
    total = db.query(Director).count()
    directors_query = db.query(Director).offset(skip).limit(size).all()
    directors = [DirectorRead.model_validate(director) for director in directors_query]
    return DirectorList(
        directors=directors,
        total=total,
        page=page,
        size=size
    )

def update_director(director_id: str, director: DirectorUpdate, db: Session) -> DirectorRead | None:
    update_director = db.query(Director).filter(Director.id == director_id).first()
    if not update_director:
        return None
    
    update_data = director.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(update_director, key, value)
        
    db.commit()
    db.refresh(update_director)
    return DirectorRead.model_validate(update_director)

def delete_director(director_id: str, db: Session) -> DirectorRead | None:
    director = db.query(Director).filter(Director.id == director_id).first()
    if not director:
        return None
    
    deleted_director = DirectorRead.model_validate(director)
    db.delete(director)
    db.commit()
    return deleted_director
