import pytest

@pytest.mark.asyncio
async def test_create_movie(client, director_fixture, genre_fixture, staff_token_fixture):
    headers = {"Authorization": f"Bearer {staff_token_fixture}"}
    director_id = director_fixture["id"]
    genre_id = genre_fixture["id"]
    response = await client.post("/movies/", json={"title": "Test Movie", "year": 2022, "rating": 5, "description": "Test description", "language": "English", "duration": 150, "trailer": "https://example.com/trailer", "image": "https://example.com/image", "director": director_id, "genres": [genre_id]}, headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Test Movie"
    assert data["year"] == 2022
    assert data["rating"] == 5
    assert data["description"] == "Test description"
    assert data["language"] == "English"
    assert data["duration"] == 150
    assert data["trailer"] == "https://example.com/trailer"
    assert data["image"] == "https://example.com/image"

@pytest.mark.asyncio
async def test_create_movie_unauthorized(client, director_fixture, genre_fixture):
    director_id = director_fixture["id"]
    genre_id = genre_fixture["id"]
    response = await client.post("/movies/", json={"title": "Test Movie", "year": 2022, "rating": 5, "description": "Test description", "language": "English", "duration": 150, "trailer": "https://example.com/trailer", "image": "https://example.com/image", "director": director_id, "genres": [genre_id]})
    assert response.status_code == 401

@pytest.mark.asyncio
async def test_create_movie_forbidden(client, director_fixture, genre_fixture, user_token_fixture):
    headers = {"Authorization": f"Bearer {user_token_fixture}"}
    director_id = director_fixture["id"]
    genre_id = genre_fixture["id"]
    response = await client.post("/movies/", json={"title": "Test Movie", "year": 2022, "rating": 5, "description": "Test description", "language": "English", "duration": 150, "trailer": "https://example.com/trailer", "image": "https://example.com/image", "director": director_id, "genres": [genre_id]}, headers=headers)
    assert response.status_code == 403

@pytest.mark.asyncio
async def test_get_movie(client, movie_fixture):
    movie_id = movie_fixture["id"]
    response = await client.get(f"/movies/{movie_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == movie_id

@pytest.mark.asyncio
async def test_get_movie_not_found(client):
    response = await client.get("/movies/non_existent_id")
    assert response.status_code == 404

@pytest.mark.asyncio
async def test_get_movie_by_title(client, movie_fixture):
    movie_id = movie_fixture["id"]
    response = await client.get(f"/movies/title/{movie_fixture['title']}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == movie_id

@pytest.mark.asyncio
async def test_get_movie_by_title_not_found(client):
    response = await client.get("/movies/title/Non Existent Movie")
    assert response.status_code == 404

@pytest.mark.asyncio
async def test_get_list_of_movies_by_title_like(client, movie_fixture):
    response = await client.get(f"/movies/title_like/{movie_fixture['title'][:5]}")
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0

@pytest.mark.asyncio
async def test_get_movies_by_genre(client, movie_fixture, genre_fixture):
    genre_id = genre_fixture["id"]
    response = await client.get(f"/movies/genre/{genre_id}")
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0

@pytest.mark.asyncio
async def test_get_movies(client):
    response = await client.get("/movies/")
    assert response.status_code == 200
    data = response.json()
    assert "movies" in data
    assert "total" in data
    assert "page" in data
    assert "size" in data

@pytest.mark.asyncio
async def test_update_movie(client, movie_fixture, staff_token_fixture):
    headers = {"Authorization": f"Bearer {staff_token_fixture}"}
    movie_id = movie_fixture["id"]
    response = await client.put(f"/movies/{movie_id}", json={"title": "Updated Movie"}, headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Updated Movie"

@pytest.mark.asyncio
async def test_update_movie_not_found(client, staff_token_fixture):
    headers = {"Authorization": f"Bearer {staff_token_fixture}"}
    response = await client.put("/movies/non_existent_id", json={"title": "Updated Movie"}, headers=headers)
    assert response.status_code == 404

@pytest.mark.asyncio
async def test_delete_movie(client, movie_fixture, staff_token_fixture):
    headers = {"Authorization": f"Bearer {staff_token_fixture}"}
    movie_id = movie_fixture["id"]
    response = await client.delete(f"/movies/{movie_id}", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == movie_id

@pytest.mark.asyncio
async def test_delete_movie_not_found(client, staff_token_fixture):
    headers = {"Authorization": f"Bearer {staff_token_fixture}"}
    response = await client.delete("/movies/non_existent_id", headers=headers)
    assert response.status_code == 404

@pytest.mark.asyncio
async def test_create_movie_director_not_found(client, genre_fixture, staff_token_fixture):
    headers = {"Authorization": f"Bearer {staff_token_fixture}"}
    genre_id = genre_fixture["id"]
    response = await client.post("/movies/", json={"title": "Test Movie", "year": 2022, "rating": 5, "description": "Test description", "language": "English", "duration": 150, "trailer": "https://example.com/trailer", "image": "https://example.com/image", "director": "non_existent_director", "genres": [genre_id]}, headers=headers)
    assert response.status_code == 400

@pytest.mark.asyncio
async def test_create_movie_genre_not_found(client, director_fixture, staff_token_fixture):
    headers = {"Authorization": f"Bearer {staff_token_fixture}"}
    director_id = director_fixture["id"]
    response = await client.post("/movies/", json={"title": "Test Movie", "year": 2022, "rating": 5, "description": "Test description", "language": "English", "duration": 150, "trailer": "https://example.com/trailer", "image": "https://example.com/image", "director": director_id, "genres": ["non_existent_genre"]}, headers=headers)
    assert response.status_code == 400

@pytest.mark.asyncio
async def test_update_movie_genre_not_found(client, movie_fixture, staff_token_fixture):
    headers = {"Authorization": f"Bearer {staff_token_fixture}"}
    movie_id = movie_fixture["id"]
    response = await client.put(f"/movies/{movie_id}", json={"genres": ["non_existent_genre"]}, headers=headers)
    assert response.status_code == 404