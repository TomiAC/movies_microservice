from datetime import datetime, timedelta
import pytest

@pytest.mark.asyncio
async def test_create_function(client, movie_fixture, auditorium_fixture, staff_token_fixture):
    headers = {"Authorization": f"Bearer {staff_token_fixture}"}
    movie_id = movie_fixture["id"]
    auditorium_id = auditorium_fixture["id"]
    start_time = datetime.now() + timedelta(days=1)
    end_time = start_time + timedelta(hours=1)
    response = await client.post("/functions/", json={"movie_id": movie_id, "auditorium_id": auditorium_id, "start_time": start_time.isoformat(), "end_time": end_time.isoformat(), "available_seats": 100, "price": 10}, headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["movie_id"] == movie_id
    assert data["auditorium_id"] == auditorium_id

@pytest.mark.asyncio
async def test_create_function_unauthorized(client, movie_fixture, auditorium_fixture):
    movie_id = movie_fixture["id"]
    auditorium_id = auditorium_fixture["id"]
    start_time = datetime.now() + timedelta(days=1)
    end_time = start_time + timedelta(hours=1)
    response = await client.post("/functions/", json={"movie_id": movie_id, "auditorium_id": auditorium_id, "start_time": start_time.isoformat(), "end_time": end_time.isoformat(), "available_seats": 100, "price": 10})
    assert response.status_code == 401

@pytest.mark.asyncio
async def test_create_function_forbidden(client, movie_fixture, auditorium_fixture, user_token_fixture):
    headers = {"Authorization": f"Bearer {user_token_fixture}"}
    movie_id = movie_fixture["id"]
    auditorium_id = auditorium_fixture["id"]
    start_time = datetime.now() + timedelta(days=1)
    end_time = start_time + timedelta(hours=1)
    response = await client.post("/functions/", json={"movie_id": movie_id, "auditorium_id": auditorium_id, "start_time": start_time.isoformat(), "end_time": end_time.isoformat(), "available_seats": 100, "price": 10}, headers=headers)
    assert response.status_code == 403

@pytest.mark.asyncio
async def test_get_function(client, function_fixture):
    function_id = function_fixture["data"]["id"]
    response = await client.get(f"/functions/{function_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == function_id

@pytest.mark.asyncio
async def test_get_all_functions(client, function_fixture):
    response = await client.get("/functions/all")
    assert response.status_code == 200
    assert response.json()["total"] > 0

@pytest.mark.asyncio
async def test_create_function_movie_not_found(client, auditorium_fixture, staff_token_fixture):
    headers = {"Authorization": f"Bearer {staff_token_fixture}"}
    auditorium_id = auditorium_fixture["id"]
    start_time = datetime.now() + timedelta(days=1)
    end_time = start_time + timedelta(hours=1)
    response = await client.post("/functions/", json={"movie_id": "non-existent-id", "auditorium_id": auditorium_id, "start_time": start_time.isoformat(), "end_time": end_time.isoformat(), "available_seats": 100, "price": 10}, headers=headers)
    assert response.status_code == 404
    assert response.json()["detail"] == "Movie not found"

@pytest.mark.asyncio
async def test_create_function_auditorium_not_found(client, movie_fixture, staff_token_fixture):
    headers = {"Authorization": f"Bearer {staff_token_fixture}"}
    movie_id = movie_fixture["id"]
    start_time = datetime.now() + timedelta(days=1)
    end_time = start_time + timedelta(hours=1)
    response = await client.post("/functions/", json={"movie_id": movie_id, "auditorium_id": "non-existent-id", "start_time": start_time.isoformat(), "end_time": end_time.isoformat(), "available_seats": 100, "price": 10}, headers=headers)
    assert response.status_code == 404
    assert response.json()["detail"] == "Auditorium not found"

@pytest.mark.asyncio
async def test_create_function_invalid_seats(client, movie_fixture, auditorium_fixture, staff_token_fixture):
    headers = {"Authorization": f"Bearer {staff_token_fixture}"}
    movie_id = movie_fixture["id"]
    auditorium_id = auditorium_fixture["id"]
    start_time = datetime.now() + timedelta(days=1)
    end_time = start_time + timedelta(hours=1)
    response = await client.post("/functions/", json={"movie_id": movie_id, "auditorium_id": auditorium_id, "start_time": start_time.isoformat(), "end_time": end_time.isoformat(), "available_seats": 200, "price": 10}, headers=headers)
    assert response.status_code == 400
    assert response.json()["detail"] == "Available seats cannot be greater than auditorium capacity"

@pytest.mark.asyncio
async def test_create_function_auditorium_not_free(client, movie_fixture, auditorium_fixture, function_fixture, staff_token_fixture):
    headers = {"Authorization": f"Bearer {staff_token_fixture}"}
    movie_id = movie_fixture["id"]
    auditorium_id = auditorium_fixture["id"]
    
    start_time = function_fixture["start_time"]
    end_time = function_fixture["end_time"]
    
    response = await client.post("/functions/", json={"movie_id": movie_id, "auditorium_id": auditorium_id, "start_time": start_time, "end_time": end_time, "available_seats": 100, "price": 10}, headers=headers)
    assert response.status_code == 400
    assert response.json()["detail"] == "Auditorium is not free"

@pytest.mark.asyncio
async def test_create_function_invalid_time(client, movie_fixture, auditorium_fixture, staff_token_fixture):
    headers = {"Authorization": f"Bearer {staff_token_fixture}"}
    movie_id = movie_fixture["id"]
    auditorium_id = auditorium_fixture["id"]
    start_time = datetime.now() + timedelta(days=1)
    end_time = start_time - timedelta(hours=1)
    response = await client.post("/functions/", json={"movie_id": movie_id, "auditorium_id": auditorium_id, "start_time": start_time.isoformat(), "end_time": end_time.isoformat(), "available_seats": 100, "price": 10}, headers=headers)
    assert response.status_code == 400
    assert response.json()["detail"] == "Start time cannot be after end time"

@pytest.mark.asyncio
async def test_create_function_past_time(client, movie_fixture, auditorium_fixture, staff_token_fixture):
    headers = {"Authorization": f"Bearer {staff_token_fixture}"}
    movie_id = movie_fixture["id"]
    auditorium_id = auditorium_fixture["id"]
    start_time = datetime.now() - timedelta(days=1)
    end_time = start_time + timedelta(hours=1)
    response = await client.post("/functions/", json={"movie_id": movie_id, "auditorium_id": auditorium_id, "start_time": start_time.isoformat(), "end_time": end_time.isoformat(), "available_seats": 100, "price": 10}, headers=headers)
    assert response.status_code == 400
    assert response.json()["detail"] == "Start time cannot be in the past"

@pytest.mark.asyncio
async def test_get_function_not_found(client):
    response = await client.get("/functions/non-existent-id")
    assert response.status_code == 404
    assert response.json()["detail"] == "Function not found"

@pytest.mark.asyncio
async def test_get_active_functions(client, function_fixture, staff_token_fixture):
    headers = {"Authorization": f"Bearer {staff_token_fixture}"}
    response = await client.get("/functions/", headers=headers)
    assert response.status_code == 200
    assert isinstance(response.json(), list)

@pytest.mark.asyncio
async def test_delete_function(client, function_fixture, staff_token_fixture):
    headers = {"Authorization": f"Bearer {staff_token_fixture}"}
    function_id = function_fixture["data"]["id"]
    response = await client.delete(f"/functions/{function_id}", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == function_id

@pytest.mark.asyncio
async def test_delete_function_not_found(client, staff_token_fixture):
    headers = {"Authorization": f"Bearer {staff_token_fixture}"}
    response = await client.delete("/functions/non-existent-id", headers=headers)
    assert response.status_code == 404
    assert response.json()["detail"] == "Function not found"
