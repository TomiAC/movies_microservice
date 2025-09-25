from sqlalchemy.orm import Session
from crud.director import create_director
from crud.genre import create_genre
from crud.movies import create_movie
from crud.cinema import create_cinema
from crud.auditorium import create_auditorium
from crud.function import create_function
from schemas.director import DirectorCreate
from schemas.genre import GenreCreate
from schemas.movies import MovieCreate
from schemas.cinema import CinemaCreate
from schemas.auditorium import AuditoriumCreate
from schemas.function import FunctionCreate

def load_data(db: Session):
    # Create directors
    director1 = create_director(DirectorCreate(name="Frank Darabont", bio="Some bio", birth_date="1959-01-28", nationality="USA", image="N/A"), db)
    director2 = create_director(DirectorCreate(name="Francis Ford Coppola", bio="Some bio", birth_date="1939-04-07", nationality="N/A", image="N/A"), db)
    director3 = create_director(DirectorCreate(name="Christopher Nolan", bio="Some bio", birth_date="1970-07-30", nationality="N/A", image="N/A"), db)

    # Create genres
    genre1 = create_genre(GenreCreate(name="Drama", description="N/A"), db)
    genre2 = create_genre(GenreCreate(name="Crime", description="N/A"), db)
    genre3 = create_genre(GenreCreate(name="Action", description="N/A"), db)
    genre4 = create_genre(GenreCreate(name="Science Fiction", description="N/A"), db)

    # Create movies
    movie1 = create_movie(MovieCreate(title="The Shawshank Redemption", year=1994, rating=9, description="N/A", image="N/A", trailer="N/A", duration=142, language="English", director=director1.id, genres=[genre1.id, genre2.id]), db)
    movie2 = create_movie(MovieCreate(title="The Godfather", year=1972, rating=9, description="N/A", image="N/A", trailer="N/A", duration=175, language="English", director=director2.id, genres=[genre1.id, genre2.id]), db)
    movie3 = create_movie(MovieCreate(title="The Dark Knight", year=2008, rating=9, description="N/A", image="N/A", trailer="N/A", duration=152, language="English", director=director3.id, genres=[genre3.id, genre2.id, genre1.id]), db)
    movie4 = create_movie(MovieCreate(title="Inception", year=2010, rating=8, description="N/A", image="N/A", trailer="N/A", duration=148, language="English", director=director3.id, genres=[genre3.id, genre4.id]), db)

    # Create cinemas
    cinema1 = create_cinema(db, CinemaCreate(name="Cinema Paradiso", location="N/A", number=1))
    cinema2 = create_cinema(db, CinemaCreate(name="Cineplex", location="N/A", number=2))

    # Create auditoriums
    auditorium1 = create_auditorium(db, AuditoriumCreate(name="Auditorium 1", cinema_id=cinema1.id, capacity=100))
    auditorium2 = create_auditorium(db, AuditoriumCreate(name="Auditorium 2", cinema_id=cinema1.id, capacity=150))
    auditorium3 = create_auditorium(db, AuditoriumCreate(name="Auditorium 3", cinema_id=cinema2.id, capacity=200))

    # Create functions
    function1 = create_function(db, FunctionCreate(movie_id=movie1.id, auditorium_id=auditorium1.id, start_time="2025-09-25 18:00:00", end_time="2025-09-25 20:22:00", price=10, available_seats=100))
    function2 = create_function(db, FunctionCreate(movie_id=movie2.id, auditorium_id=auditorium1.id, start_time="2025-09-25 21:00:00", end_time="2025-09-25 23:55:00", price=10, available_seats=100))
    function3 = create_function(db, FunctionCreate(movie_id=movie3.id, auditorium_id=auditorium2.id, start_time="2025-09-25 19:00:00", end_time="2025-09-25 21:32:00", price=12, available_seats=150))
    function4 = create_function(db, FunctionCreate(movie_id=movie4.id, auditorium_id=auditorium3.id, start_time="2025-09-25 20:00:00", end_time="2025-09-25 22:28:00", price=12, available_seats=200))