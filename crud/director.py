from models.director import Director
from schemas.director import DirectorCreate, DirectorRead, DirectorUpdate, DirectorList
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

async def create_director(director: DirectorCreate, db: AsyncSession) -> DirectorRead:
    new_director = Director(**director.model_dump())
    db.add(new_director)
    await db.commit()
    await db.refresh(new_director)
    return DirectorRead.model_validate(new_director)

async def get_director(director_id: str, db: AsyncSession) -> DirectorRead | None:
    result = await db.execute(select(Director).filter(Director.id == director_id))
    director = result.scalars().first()
    if not director:
        return None
    return DirectorRead.model_validate(director)

async def get_directors(db: AsyncSession, page: int = 1, size: int = 10) -> DirectorList:
    skip = (page - 1) * size
    
    total_result = await db.execute(select(func.count(Director.id)))
    total = total_result.scalar_one()

    directors_query = await db.execute(select(Director).offset(skip).limit(size))
    directors = [DirectorRead.model_validate(director) for director in directors_query.scalars().all()]
    
    return DirectorList(
        directors=directors,
        total=total,
        page=page,
        size=size
    )

async def update_director(director_id: str, director: DirectorUpdate, db: AsyncSession) -> DirectorRead | None:
    result = await db.execute(select(Director).filter(Director.id == director_id))
    update_director = result.scalars().first()
    
    if not update_director:
        return None
    
    update_data = director.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(update_director, key, value)
        
    await db.commit()
    await db.refresh(update_director)
    return DirectorRead.model_validate(update_director)

async def delete_director(director_id: str, db: AsyncSession) -> DirectorRead | None:
    result = await db.execute(select(Director).filter(Director.id == director_id))
    director = result.scalars().first()
    if not director:
        return None
    
    deleted_director = DirectorRead.model_validate(director)
    await db.delete(director)
    await db.commit()
    return deleted_director
