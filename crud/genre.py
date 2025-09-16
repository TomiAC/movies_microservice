from models.genre import Genre
from schemas.genre import GenreCreate, GenreRead, GenreUpdate, GenreList
from typing import List
from sqlalchemy.orm import Session

def create_genre(genre: GenreCreate, db: Session) -> GenreRead:
    new_genre = Genre(**genre.model_dump())
    db.add(new_genre)
    db.commit()
    db.refresh(new_genre)
    return GenreRead.model_validate(new_genre)

def get_genre(genre_id: str, db: Session) -> GenreRead | None:
    genre = db.query(Genre).filter(Genre.id == genre_id).first()
    if not genre:
        return None
    return GenreRead.model_validate(genre)

def get_genres(db: Session, page: int = 1, size: int = 10) -> GenreList:
    skip = (page - 1) * size
    total = db.query(Genre).count()
    genres = db.query(Genre).offset(skip).limit(size).all()
    return GenreList(
        genres=[GenreRead.model_validate(genre) for genre in genres],
        total=total,
        page=page,
        size=size
    )

def get_genre_by_name(name: str, db: Session) -> GenreRead | None:
    genre = db.query(Genre).filter(Genre.name == name).first()
    if not genre:
        return None
    return GenreRead.model_validate(genre)

def update_genre(genre_id: str, genre: GenreUpdate, db: Session) -> GenreRead:
    existing_genre = db.query(Genre).filter(Genre.id == genre_id).first()
    if not existing_genre:
        return None
    
    update_data = genre.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(existing_genre, key, value)

    db.commit()
    db.refresh(existing_genre)
    return GenreRead.model_validate(existing_genre)

def delete_genre(genre_id: str, db: Session) -> GenreRead:
    genre = db.query(Genre).filter(Genre.id == genre_id).first()
    if not genre:
        return None
    db.delete(genre)
    db.commit()
    return GenreRead.model_validate(genre)