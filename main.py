from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from routers.genre import genre_router
from routers.director import director_router
from routers.movies import movie_router
from routers.cinema import cinema_router
from routers.auditorium import auditorium_router
from routers.function import function_router
from database import Base, engine
from dependencies import get_db
from data_loader import load_data

app = FastAPI()

Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)

# @app.on_event("startup")
# def on_startup():
#     db = next(get_db())
#     load_data(db)

app.include_router(genre_router)
app.include_router(director_router)
app.include_router(movie_router)
app.include_router(cinema_router)
app.include_router(auditorium_router)
app.include_router(function_router)

@app.get("/")
def welcome():
    return {"message": "Welcome to the Movie API!"}