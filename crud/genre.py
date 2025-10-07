from models.genre import Genre
from schemas.genre import GenreCreate, GenreRead, GenreUpdate, GenreList
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.sql import func

async def create_genre(genre: GenreCreate, db: AsyncSession) -> GenreRead:
    new_genre = Genre(**genre.model_dump())
    db.add(new_genre)
    await db.commit()
    await db.refresh(new_genre)
    return GenreRead.model_validate(new_genre)

async def get_genre(genre_id: str, db: AsyncSession) -> GenreRead | None:
    result = await db.execute(select(Genre).filter(Genre.id == genre_id))
    genre = result.scalar_one_or_none()
    if not genre:
        return None
    return GenreRead.model_validate(genre)

async def get_genres(db: AsyncSession, page: int = 1, size: int = 10) -> GenreList:
    skip = (page - 1) * size
    total_result = await db.execute(select(func.count(Genre.id)))
    total = total_result.scalar()
    genres_result = await db.execute(select(Genre).offset(skip).limit(size))
    genres = genres_result.scalars().all()
    return GenreList(
        genres=[GenreRead.model_validate(genre) for genre in genres],
        total=total,
        page=page,
        size=size
    )

async def get_genre_by_name(name: str, db: AsyncSession) -> GenreRead | None:
    result = await db.execute(select(Genre).filter(Genre.name == name))
    genre = result.scalar_one_or_none()
    if not genre:
        return None
    return GenreRead.model_validate(genre)

async def update_genre(genre_id: str, genre: GenreUpdate, db: AsyncSession) -> GenreRead:
    result = await db.execute(select(Genre).filter(Genre.id == genre_id))
    existing_genre = result.scalar_one_or_none()
    if not existing_genre:
        return None
    
    update_data = genre.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(existing_genre, key, value)

    await db.commit()
    await db.refresh(existing_genre)
    return GenreRead.model_validate(existing_genre)

async def delete_genre(genre_id: str, db: AsyncSession) -> GenreRead:
    result = await db.execute(select(Genre).filter(Genre.id == genre_id))
    genre = result.scalar_one_or_none()
    if not genre:
        return None
    await db.delete(genre)
    await db.commit()
    return GenreRead.model_validate(genre)