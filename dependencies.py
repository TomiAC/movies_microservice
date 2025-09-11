from database import SessionLocal
from fastapi import HTTPException, status

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def has_role(required_role: str, user_role: str):
    if user_role != required_role:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Operation not permitted"
        )
    return True
