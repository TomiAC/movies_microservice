from crud.function import create_function, get_function, get_functions, update_function, delete_function, check_auditorium_free
from crud.movies import get_movie
from crud.auditorium import get_auditorium
from schemas.function import FunctionCreate, FunctionRead, FunctionUpdate, FunctionList
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from datetime import datetime

function_router = APIRouter(prefix="/functions", tags=["functions"])

@function_router.post("/", response_model=FunctionRead)
def function_create_endpoint(function: FunctionCreate, db: Session = Depends(get_db)) -> FunctionRead:
    movie = get_movie(function.movie_id, db)
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    auditorium = get_auditorium(db, function.auditorium_id)
    if not auditorium:
        raise HTTPException(status_code=404, detail="Auditorium not found")
    if function.available_seats > auditorium.capacity:
        raise HTTPException(status_code=400, detail="Available seats cannot be greater than auditorium capacity")
    if not check_auditorium_free(db, function.auditorium_id, function.start_time, function.end_time):
        raise HTTPException(status_code=400, detail="Auditorium is not free")
    if function.start_time > function.end_time:
        raise HTTPException(status_code=400, detail="Start time cannot be after end time")
    if function.start_time < datetime.now():
        raise HTTPException(status_code=400, detail="Start time cannot be in the past")
    function.start_time = function.start_time.strftime("%Y-%m-%d %H:%M:%S")
    function.end_time = function.end_time.strftime("%Y-%m-%d %H:%M:%S")
    db_function = create_function(db, function)
    if not db_function:
        raise HTTPException(status_code=400, detail="Failed to create function")
    return FunctionRead.model_validate(db_function)

@function_router.get("/{function_id}", response_model=FunctionRead)
def function_get_endpoint(function_id: str, db: Session = Depends(get_db)) -> FunctionRead:
    db_function = get_function(db, function_id)
    if not db_function:
        raise HTTPException(status_code=404, detail="Function not found")
    return

@function_router.get("/", response_model=FunctionList)
def function_get_all_endpoint(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)) -> FunctionList:
    return get_functions(db, skip, limit)
