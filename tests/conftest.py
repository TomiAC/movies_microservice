import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from main import app
from database import Base
from dependencies import get_db

# Setup for an in-memory SQLite database for testing
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

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
