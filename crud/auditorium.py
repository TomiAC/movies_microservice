from models.auditorium import Auditorium
from schemas.auditorium import AuditoriumCreate, AuditoriumRead, AuditoriumUpdate
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from typing import List, Optional

async def create_auditorium(db: AsyncSession, auditorium: AuditoriumCreate) -> AuditoriumRead:
    db_auditorium = Auditorium(**auditorium.model_dump())
    db.add(db_auditorium)
    await db.commit()
    await db.refresh(db_auditorium)
    return AuditoriumRead.model_validate(db_auditorium)

async def get_auditorium(db: AsyncSession, auditorium_id: str) -> AuditoriumRead | None:
    result = await db.execute(select(Auditorium).filter(Auditorium.id == auditorium_id))
    db_auditorium = result.scalar_one_or_none()
    if db_auditorium:
        return AuditoriumRead.model_validate(db_auditorium)
    return None

async def get_auditoriums(db: AsyncSession, skip: int = 0, limit: int = 100) -> dict:
    total_result = await db.execute(select(func.count()).select_from(Auditorium))
    total = total_result.scalar_one()

    result = await db.execute(select(Auditorium).offset(skip).limit(limit))
    db_auditoriums = result.scalars().all()
    
    auditoriums = [AuditoriumRead.model_validate(auditorium) for auditorium in db_auditoriums]
    page = (skip // limit) + 1 if limit > 0 else 1
    return {
        "auditoriums": auditoriums,
        "total": total,
        "page": page,
        "size": limit,
    }

async def update_auditorium(db: AsyncSession, auditorium_id: str, auditorium_update: AuditoriumUpdate) -> AuditoriumRead | None:
    result = await db.execute(select(Auditorium).filter(Auditorium.id == auditorium_id))
    db_auditorium = result.scalar_one_or_none()
    if not db_auditorium:
        return None
    update_data = auditorium_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_auditorium, key, value)
    await db.commit()
    await db.refresh(db_auditorium)
    return AuditoriumRead.model_validate(db_auditorium)

async def delete_auditorium(db: AsyncSession, auditorium_id: str) -> AuditoriumRead | None:
    result = await db.execute(select(Auditorium).filter(Auditorium.id == auditorium_id))
    db_auditorium = result.scalar_one_or_none()
    if not db_auditorium:
        return None
    await db.delete(db_auditorium)
    await db.commit()
    return AuditoriumRead.model_validate(db_auditorium)