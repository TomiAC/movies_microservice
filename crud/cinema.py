from schemas.cinema import CinemaCreate, CinemaUpdate, CinemaRead
from models.cinema import Cinema
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from typing import List

async def create_cinema(db: AsyncSession, cinema: CinemaCreate) -> CinemaRead:
    db_cinema = Cinema(**cinema.model_dump())
    db.add(db_cinema)
    await db.commit()
    await db.refresh(db_cinema)
    return CinemaRead.model_validate(db_cinema)

async def get_cinema(db: AsyncSession, cinema_id: str) -> CinemaRead:
    result = await db.execute(select(Cinema).filter(Cinema.id == cinema_id))
    db_cinema = result.scalar_one_or_none()
    if not db_cinema:
        return None
    return CinemaRead.model_validate(db_cinema)

async def get_cinemas(db: AsyncSession, skip: int = 0, limit: int = 100) -> dict:
    total_result = await db.execute(select(func.count()).select_from(Cinema))
    total = total_result.scalar_one()
    
    result = await db.execute(select(Cinema).offset(skip).limit(limit))
    db_cinemas = result.scalars().all()
    
    cinemas = [CinemaRead.model_validate(cinema) for cinema in db_cinemas]
    page = (skip // limit) + 1 if limit > 0 else 1
    return {
        "cinemas": cinemas,
        "total": total,
        "page": page,
        "size": limit,
    }

async def update_cinema(db: AsyncSession, cinema_id: str, cinema_update: CinemaUpdate) -> CinemaRead:
    result = await db.execute(select(Cinema).filter(Cinema.id == cinema_id))
    db_cinema = result.scalar_one_or_none()
    
    if not db_cinema:
        return None
        
    update_data = cinema_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_cinema, key, value)
        
    await db.commit()
    await db.refresh(db_cinema)
    return CinemaRead.model_validate(db_cinema)

async def delete_cinema(db: AsyncSession, cinema_id: str) -> CinemaRead:
    result = await db.execute(select(Cinema).filter(Cinema.id == cinema_id))
    db_cinema = result.scalar_one_or_none()

    if not db_cinema:
        return None
        
    await db.delete(db_cinema)
    await db.commit()
    return CinemaRead.model_validate(db_cinema)