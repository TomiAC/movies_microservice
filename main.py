from fastapi import FastAPI
from routers.genre import genre_router
from routers.director import director_router
from routers.movies import movie_router
from routers.cinema import cinema_router
from database import Base, engine

app = FastAPI()

Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)

app.include_router(genre_router)
app.include_router(director_router)
app.include_router(movie_router)
app.include_router(cinema_router)

@app.get("/")
def welcome():
    return {"message": "Welcome to the Movie API!"}