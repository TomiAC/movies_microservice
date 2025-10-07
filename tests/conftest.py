import os
os.environ['TESTING'] = 'True'

import pytest_asyncio
import asyncio
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from main import app
from database import Base
from dependencies import get_db
from datetime import datetime, timedelta
import jwt
from schemas.user import UserRole
from dotenv import load_dotenv
import uuid

load_dotenv()

# Use an in-memory SQLite database for testing
ASYNC_SQLALCHEMY_DATABASE_URL = "sqlite+aiosqlite:///:memory:"

SECRET_KEY = os.environ.get("SECRET_KEY")
ALGORITHM = os.environ.get("ALGORITHM")

engine = create_async_engine(ASYNC_SQLALCHEMY_DATABASE_URL)

TestingSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)

async def override_get_db():
    async with TestingSessionLocal() as session:
        yield session

app.dependency_overrides[get_db] = override_get_db

@pytest_asyncio.fixture(scope="function")
async def client():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as c:
        yield c

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

@pytest_asyncio.fixture
def admin_token_fixture():
    return create_access_token(data={"user_id": "admin", "role": UserRole.ADMIN.value})

@pytest_asyncio.fixture
def staff_token_fixture():
    return create_access_token(data={"user_id": "staff", "role": UserRole.STAFF.value})

@pytest_asyncio.fixture
def user_token_fixture():
    return create_access_token(data={"user_id": "user", "role": UserRole.USER.value})

@pytest_asyncio.fixture
async def director_fixture(client, staff_token_fixture):
    headers = {"Authorization": f"Bearer {staff_token_fixture}"}
    response = await client.post("/directors/", json={"name": f"John Doe {uuid.uuid4()}", "birth_date": "1970-01-01", "nationality": "USA", "bio": "Some bio"}, headers=headers)
    assert response.status_code == 200
    return response.json()

@pytest_asyncio.fixture
async def genre_fixture(client, staff_token_fixture):
    headers = {"Authorization": f"Bearer {staff_token_fixture}"}
    response = await client.post("/genres/", json={"name": f"Action {uuid.uuid4()}", "description": "Action movies"}, headers=headers)
    assert response.status_code == 200
    return response.json()

@pytest_asyncio.fixture
async def cinema_fixture(client, admin_token_fixture):
    headers = {"Authorization": f"Bearer {admin_token_fixture}"}
    response = await client.post("/cinemas/", json={"name": f"Cinema City {uuid.uuid4()}", "location": "123 Main St", "number": 1}, headers=headers)
    assert response.status_code == 200
    return response.json()

@pytest_asyncio.fixture
async def auditorium_fixture(client, cinema_fixture, admin_token_fixture):
    cinema_id = cinema_fixture["id"]
    headers = {"Authorization": f"Bearer {admin_token_fixture}"}
    response = await client.post("/auditoriums/", json={"name": f"1A {uuid.uuid4()}", "cinema_id": cinema_id, "capacity": 100}, headers=headers)
    assert response.status_code == 200
    return response.json()

@pytest_asyncio.fixture
async def movie_fixture(client, director_fixture, genre_fixture, staff_token_fixture):
    director_id = director_fixture["id"]
    genre_id = genre_fixture["id"]
    headers = {"Authorization": f"Bearer {staff_token_fixture}"}
    response = await client.post("/movies/", json={"title": f"Test Movie {uuid.uuid4()}", "year": "2022", "rating": 5, "description": "Test description", "language": "English", "duration": 1, "trailer": "https://example.com/trailer", "image": "https://example.com/image", "director": director_id, "genres": [genre_id]}, headers=headers)
    assert response.status_code == 200
    return response.json()

@pytest_asyncio.fixture
async def function_fixture(client, movie_fixture, auditorium_fixture, staff_token_fixture):
    movie_id = movie_fixture["id"]
    auditorium_id = auditorium_fixture["id"]
    headers = {"Authorization": f"Bearer {staff_token_fixture}"}
    
    start_time = datetime.now() + timedelta(days=1)
    end_time = start_time + timedelta(hours=1)
    
    start_time_iso = start_time.isoformat()
    end_time_iso = end_time.isoformat()

    response = await client.post(
        "/functions/",
        json={
            "movie_id": movie_id,
            "auditorium_id": auditorium_id,
            "start_time": start_time_iso,
            "end_time": end_time_iso,
            "available_seats": 100,
            "price": 10,
        },
        headers=headers,
    )
    assert response.status_code == 200
    response_data = response.json()
    
    return {
        "data": response_data,
        "start_time": start_time_iso,
        "end_time": end_time_iso,
    }
