import os
from fastapi import FastAPI
from contextlib import asynccontextmanager
from database import Base, engine
from dependencies import get_db
from data_loader import load_data
from routers.genre import genre_router
from routers.director import director_router
from routers.movies import movie_router
from routers.cinema import cinema_router
from routers.auditorium import auditorium_router
from routers.function import function_router

Base.metadata.create_all(bind=engine)

# Get the testing environment variable
TESTING = os.environ.get("TESTING")

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup logic
    print("Startup logic running...")
    Base.metadata.create_all(bind=engine)
    if not TESTING:
        db = next(get_db())
        load_data(db)
    yield
    # Shutdown logic (if any)
    print("Shutdown logic running...")

app = FastAPI(lifespan=lifespan)

app.include_router(genre_router)
app.include_router(director_router)
app.include_router(movie_router)
app.include_router(cinema_router)
app.include_router(auditorium_router)
app.include_router(function_router)

@app.get("/")
def welcome():
    return {"message": "Welcome to the Movie API!"}