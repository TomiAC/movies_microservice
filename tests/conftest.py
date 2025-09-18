# Setup for an in-memory SQLite database for testing
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from main import app
from database import Base
from dependencies import get_db

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Override the get_db dependency to use the test database
def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

@pytest.fixture(scope="function")
def client():
    # Create the tables in the test database
    Base.metadata.create_all(bind=engine)
    
    # Yield a TestClient instance
    with TestClient(app) as c:
        yield c
        
    # Drop the tables after the tests are done
    Base.metadata.drop_all(bind=engine)

@pytest.fixture
def director_fixture(client):
    response = client.post("/directors/", json={"name": "John Doe", "birth_date": "1970-01-01", "nationality": "USA", "bio": "Some bio"})
    assert response.status_code == 200
    return response.json()

@pytest.fixture
def genre_fixture(client):
    response = client.post("/genres/", json={"name": "Action", "description": "Action movies"})
    assert response.status_code == 200
    return response.json()

@pytest.fixture
def cinema_fixture(client):
    response = client.post("/cinemas/", json={"name": "Cinema City", "location": "123 Main St", "number": 1})
    assert response.status_code == 200
    return response.json()

@pytest.fixture
def auditorium_fixture(client, cinema_fixture):
    """Fixture to create an auditorium and return its data."""
    cinema_id = cinema_fixture["id"]
    response = client.post("/auditoriums/", json={"name": "1A", "cinema_id": cinema_id, "capacity": 100})
    assert response.status_code == 200
    return response.json()

@pytest.fixture
def movie_fixture(client, director_fixture, genre_fixture):
    """Fixture to create a movie and return its data."""
    director_id = director_fixture["id"]
    genre_id = genre_fixture["id"]
    response = client.post("/movies/", json={"title": "Test Movie", "year": "2022", "rating": 5, "description": "Test description", "language": "English", "duration": 1, "trailer": "https://example.com/trailer", "image": "https://example.com/image", "director": director_id, "genres": [genre_id]})
    assert response.status_code == 200
    return response.json()

@pytest.fixture
def function_fixture(client, movie_fixture, auditorium_fixture):
    """Fixture to create a function and return its data."""
    movie_id = movie_fixture["id"]
    auditorium_id = auditorium_fixture["id"]
    response = client.post("/functions/", json={"movie_id": movie_id, "auditorium_id": auditorium_id, "start_time": "2025-09-20 15:00:00", "end_time": "2025-09-20 16:00:00", "available_seats": 100, "price": 10})
    assert response.status_code == 200
    response_data = response.json()
    return response_data