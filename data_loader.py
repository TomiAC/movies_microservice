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
    director1 = create_director(DirectorCreate(name="Frank Darabont", bio="Some bio", birth_date="1959-01-28", nationality="USA", image="https://example.com/frank_darabont.jpg"), db)
    director2 = create_director(DirectorCreate(name="Francis Ford Coppola", bio="Some bio", birth_date="1939-04-07", nationality="USA", image="https://example.com/francis_ford_coppola.jpg"), db)
    director3 = create_director(DirectorCreate(name="Christopher Nolan", bio="Some bio", birth_date="1970-07-30", nationality="British", image="https://example.com/christopher_nolan.jpg"), db)

    # Create genres
    genre1 = create_genre(GenreCreate(name="Drama", description="Movies that are serious in tone."), db)
    genre2 = create_genre(GenreCreate(name="Crime", description="Movies that focus on criminal activity."), db)
    genre3 = create_genre(GenreCreate(name="Action", description="Movies with a lot of action and adventure."), db)
    genre4 = create_genre(GenreCreate(name="Science Fiction", description="Movies with futuristic or imaginative themes."), db)

    # Create movies
    movie1 = create_movie(MovieCreate(title="The Shawshank Redemption", year=1994, rating=9, description="Two imprisoned men bond over a number of years, finding solace and eventual redemption through acts of common decency.", image="https://example.com/the_shawshank_redemption.jpg", trailer="https://example.com/the_shawshank_redemption_trailer.mp4", duration=142, language="English", director=director1.id, genres=[genre1.id, genre2.id]), db)
    movie2 = create_movie(MovieCreate(title="The Godfather", year=1972, rating=9, description="The aging patriarch of an organized crime dynasty transfers control of his clandestine empire to his reluctant son.", image="https://example.com/the_godfather.jpg", trailer="https://example.com/the_godfather_trailer.mp4", duration=175, language="English", director=director2.id, genres=[genre1.id, genre2.id]), db)
    movie3 = create_movie(MovieCreate(title="The Dark Knight", year=2008, rating=9, description="When the menace known as the Joker wreaks havoc and chaos on the people of Gotham, Batman must accept one of the greatest psychological and physical tests of his ability to fight injustice.", image="https://example.com/the_dark_knight.jpg", trailer="https://example.com/the_dark_knight_trailer.mp4", duration=152, language="English", director=director3.id, genres=[genre3.id, genre2.id, genre1.id]), db)
    movie4 = create_movie(MovieCreate(title="Inception", year=2010, rating=8, description="A thief who steals corporate secrets through the use of dream-sharing technology is given the inverse task of planting an idea into the mind of a C.E.O.", image="https://example.com/inception.jpg", trailer="https://example.com/inception_trailer.mp4", duration=148, language="English", director=director3.id, genres=[genre3.id, genre4.id]), db)

    # Create cinemas
    cinema1 = create_cinema(db, CinemaCreate(name="Cinema Paradiso", location="123 Main Street, Springfield", number=1))
    cinema2 = create_cinema(db, CinemaCreate(name="Cineplex", location="456 Oak Avenue, Shelbyville", number=2))

    # Create auditoriums
    auditorium1 = create_auditorium(db, AuditoriumCreate(name="Auditorium 1", cinema_id=cinema1.id, capacity=100))
    auditorium2 = create_auditorium(db, AuditoriumCreate(name="Auditorium 2", cinema_id=cinema1.id, capacity=150))
    auditorium3 = create_auditorium(db, AuditoriumCreate(name="Auditorium 3", cinema_id=cinema2.id, capacity=200))

    # Create functions
    function1 = create_function(db, FunctionCreate(movie_id=movie1.id, auditorium_id=auditorium1.id, start_time="2025-09-25 18:00:00", end_time="2025-09-25 20:22:00", price=10, available_seats=100))
    function2 = create_function(db, FunctionCreate(movie_id=movie2.id, auditorium_id=auditorium1.id, start_time="2025-09-25 21:00:00", end_time="2025-09-25 23:55:00", price=10, available_seats=100))
    function3 = create_function(db, FunctionCreate(movie_id=movie3.id, auditorium_id=auditorium2.id, start_time="2025-09-25 19:00:00", end_time="2025-09-25 21:32:00", price=12, available_seats=150))
    function4 = create_function(db, FunctionCreate(movie_id=movie4.id, auditorium_id=auditorium3.id, start_time="2025-09-25 20:00:00", end_time="2025-09-25 22:28:00", price=12, available_seats=200))
