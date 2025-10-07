from fastapi import APIRouter, Depends, HTTPException
from schemas.auditorium import AuditoriumCreate, AuditoriumRead, AuditoriumUpdate, AuditoriumList
from crud.auditorium import create_auditorium, get_auditorium, get_auditoriums, update_auditorium, delete_auditorium
from crud.cinema import get_cinema
from dependencies import get_db, RoleRequired
from schemas.user import UserRole
from sqlalchemy.ext.asyncio import AsyncSession

auditorium_router = APIRouter(prefix="/auditoriums", tags=["auditoriums"])

@auditorium_router.post("/", response_model=AuditoriumRead)
async def create_auditorium_endpoint(auditorium: AuditoriumCreate, db: AsyncSession = Depends(get_db), role: UserRole = Depends(RoleRequired([UserRole.ADMIN]))):
    cinema = await get_cinema(db, auditorium.cinema_id)
    if not cinema:
        raise HTTPException(status_code=400, detail="Cinema does not exist")
    new_auditorium = await create_auditorium(db, auditorium)
    if not new_auditorium:
        raise HTTPException(status_code=400, detail="Failed to create auditorium")
    return new_auditorium

@auditorium_router.get("/{auditorium_id}", response_model=AuditoriumRead)
async def get_auditorium_endpoint(auditorium_id: str, db: AsyncSession = Depends(get_db)):
    auditorium = await get_auditorium(db, auditorium_id)
    if not auditorium:
        raise HTTPException(status_code=404, detail="Auditorium not found")
    return auditorium

@auditorium_router.get("/", response_model=AuditoriumList)
async def get_auditoriums_endpoint(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    auditoriums_data = await get_auditoriums(db, skip=skip, limit=limit)
    return AuditoriumList(**auditoriums_data)

@auditorium_router.put("/{auditorium_id}", response_model=AuditoriumRead)
async def update_auditorium_endpoint(auditorium_id: str, auditorium_update: AuditoriumUpdate, db: AsyncSession = Depends(get_db), role: UserRole = Depends(RoleRequired([UserRole.ADMIN]))):
    updated_auditorium = await update_auditorium(db, auditorium_id, auditorium_update)
    if not updated_auditorium:
        raise HTTPException(status_code=404, detail="Auditorium not found")
    return updated_auditorium

@auditorium_router.delete("/{auditorium_id}", response_model=AuditoriumRead)
async def delete_auditorium_endpoint(auditorium_id: str, db: AsyncSession = Depends(get_db), role: UserRole = Depends(RoleRequired([UserRole.ADMIN]))):
    deleted_auditorium = await delete_auditorium(db, auditorium_id)
    if not deleted_auditorium:
        raise HTTPException(status_code=404, detail="Auditorium not found")
    return deleted_auditorium