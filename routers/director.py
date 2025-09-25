from crud.director import create_director, get_director, get_directors, update_director, delete_director
from fastapi import APIRouter, HTTPException, Depends
from typing import List
from schemas.director import DirectorCreate, DirectorRead, DirectorUpdate, DirectorList
from dependencies import get_db, RoleRequired
from sqlalchemy.orm import Session
from datetime import datetime, date
from schemas.user import UserRole

director_router = APIRouter(prefix="/directors", tags=["directors"])

@director_router.post("/", response_model=DirectorRead)
async def create_director_endpoint(director: DirectorCreate, db: Session = Depends(get_db), role: UserRole = Depends(RoleRequired([UserRole.ADMIN, UserRole.STAFF]))):
    if director.birth_date:
        director.birth_date = director.birth_date.strftime("%Y-%m-%d")
    new_director = create_director(director, db)
    if not new_director:
        raise HTTPException(status_code=400, detail="Director could not be created")
    return new_director

@director_router.get("/{director_id}", response_model=DirectorRead)
async def get_director_endpoint(director_id: str, db: Session = Depends(get_db)):
    director = get_director(director_id, db)
    if not director:
        raise HTTPException(status_code=404, detail="Director not found")
    return director

@director_router.get("/", response_model=DirectorList)
async def get_directors_endpoint(page: int = 1, size: int = 10, db: Session = Depends(get_db)):
    return get_directors(db, page, size)

@director_router.put("/{director_id}", response_model=DirectorRead)
async def update_director_endpoint(director_id: str, director: DirectorUpdate, db: Session = Depends(get_db), role: UserRole = Depends(RoleRequired([UserRole.ADMIN, UserRole.STAFF]))):
    updated_director = update_director(director_id, director, db)
    if not updated_director:
        raise HTTPException(status_code=404, detail="Director not found")
    return updated_director

@director_router.delete("/{director_id}", response_model=DirectorRead)
async def delete_director_endpoint(director_id: str, db: Session = Depends(get_db), role: UserRole = Depends(RoleRequired([UserRole.ADMIN, UserRole.STAFF]))):
    deleted_director = delete_director(director_id, db)
    if not deleted_director:
        raise HTTPException(status_code=404, detail="Director not found")
    return deleted_director