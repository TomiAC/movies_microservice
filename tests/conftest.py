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
import os
from datetime import datetime, timedelta
import jwt
from schemas.user import UserRole
from dotenv import load_dotenv
import uuid

load_dotenv()

SECRET_KEY = os.environ.get("SECRET_KEY")
ALGORITHM = os.environ.get("ALGORITHM")

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

@pytest.fixture(scope="function")
def client():
    Base.metadata.create_all(bind=engine)
    with TestClient(app) as c:
        yield c
    Base.metadata.drop_all(bind=engine)

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

@pytest.fixture
def admin_token_fixture():
    return create_access_token(data={"user_id": "admin", "role": UserRole.ADMIN.value})

@pytest.fixture
def staff_token_fixture():
    return create_access_token(data={"user_id": "staff", "role": UserRole.STAFF.value})

@pytest.fixture
def user_token_fixture():
    return create_access_token(data={"user_id": "user", "role": UserRole.USER.value})

@pytest.fixture
def director_fixture(client, staff_token_fixture):
    headers = {"Authorization": f"Bearer {staff_token_fixture}"}
    response = client.post("/directors/", json={"name": f"John Doe {uuid.uuid4()}", "birth_date": "1970-01-01", "nationality": "USA", "bio": "Some bio"}, headers=headers)
    assert response.status_code == 200
    return response.json()

@pytest.fixture
def genre_fixture(client, staff_token_fixture):
    headers = {"Authorization": f"Bearer {staff_token_fixture}"}
    response = client.post("/genres/", json={"name": f"Action {uuid.uuid4()}", "description": "Action movies"}, headers=headers)
    assert response.status_code == 200
    return response.json()

@pytest.fixture
def cinema_fixture(client, admin_token_fixture):
    headers = {"Authorization": f"Bearer {admin_token_fixture}"}
    response = client.post("/cinemas/", json={"name": f"Cinema City {uuid.uuid4()}", "location": "123 Main St", "number": 1}, headers=headers)
    assert response.status_code == 200
    return response.json()

@pytest.fixture
def auditorium_fixture(client, cinema_fixture, admin_token_fixture):
    """Fixture to create an auditorium and return its data."""
    cinema_id = cinema_fixture["id"]
    headers = {"Authorization": f"Bearer {admin_token_fixture}"}
    response = client.post("/auditoriums/", json={"name": f"1A {uuid.uuid4()}", "cinema_id": cinema_id, "capacity": 100}, headers=headers)
    assert response.status_code == 200
    return response.json()

@pytest.fixture
def movie_fixture(client, director_fixture, genre_fixture, staff_token_fixture):
    """Fixture to create a movie and return its data."""
    director_id = director_fixture["id"]
    genre_id = genre_fixture["id"]
    headers = {"Authorization": f"Bearer {staff_token_fixture}"}
    response = client.post("/movies/", json={"title": f"Test Movie {uuid.uuid4()}", "year": "2022", "rating": 5, "description": "Test description", "language": "English", "duration": 1, "trailer": "https://example.com/trailer", "image": "https://example.com/image", "director": director_id, "genres": [genre_id]}, headers=headers)
    assert response.status_code == 200
    return response.json()

@pytest.fixture
def function_fixture(client, movie_fixture, auditorium_fixture, staff_token_fixture):
    """Fixture to create a function and return its data."""
    movie_id = movie_fixture["id"]
    auditorium_id = auditorium_fixture["id"]
    headers = {"Authorization": f"Bearer {staff_token_fixture}"}
    response = client.post("/functions/", json={"movie_id": movie_id, "auditorium_id": auditorium_id, "start_time": "2025-09-30 15:00:00", "end_time": "2025-09-30 16:00:00", "available_seats": 100, "price": 10}, headers=headers)
    assert response.status_code == 200
    response_data = response.json()
    return response_data
