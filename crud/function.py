from models.function import Function
from schemas.function import FunctionCreate, FunctionList, FunctionUpdate, FunctionRead
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime

def create_function(db: Session, function: FunctionCreate) -> FunctionRead:
    db_function = Function(**function.model_dump())
    db.add(db_function)
    db.commit()
    db.refresh(db_function)
    db_function.start_time = datetime.strptime(db_function.start_time, "%Y-%m-%d %H:%M:%S")
    db_function.end_time = datetime.strptime(db_function.end_time, "%Y-%m-%d %H:%M:%S")
    return FunctionRead.model_validate(db_function)

def get_function(db: Session, function_id: str) -> FunctionRead | None:
    db_function = db.query(Function).filter(Function.id == function_id).first()
    if not db_function:
        return None
    return FunctionRead.model_validate(db_function)

def get_functions(db: Session, skip: int = 0, limit: int = 100) -> FunctionList:
    total = db.query(Function).count()
    db_functions = db.query(Function).offset(skip).limit(limit).all()
    functions = [FunctionRead.model_validate(function) for function in db_functions]
    page = (skip // limit) + 1 if limit > 0 else 1
    return {
        "functions": functions,
        "total": total,
        "page": page,
        "size": limit,
    }

def delete_function(db: Session, function_id: str) -> FunctionRead | None:
    db_function = db.query(Function).filter(Function.id == function_id).first()
    if not db_function:
        return None
    db.delete(db_function)
    db.commit()
    return FunctionRead.model_validate(db_function)

def check_auditorium_free(db: Session, auditorium_id: str, start_time: datetime, end_time: datetime):
    format_string = "%Y-%m-%d %H:%M:%S"
    auditorium_functions_db = db.query(Function).filter(Function.auditorium_id == auditorium_id).all()
    if not auditorium_functions_db:
        return True
    for function in auditorium_functions_db:
        start_time_datetime = datetime.strptime(function.start_time, format_string)
        end_time_datetime = datetime.strptime(function.end_time, format_string)
        # An overlap occurs if the new function starts before the existing one ends,
        # and the new function ends after the existing one starts.
        if (start_time < end_time_datetime) and (end_time > start_time_datetime):
            return False  # Overlap found, auditorium is not free
    return True  # No overlaps found