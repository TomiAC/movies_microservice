def test_create_function(client, movie_fixture, auditorium_fixture, staff_token_fixture):
    headers = {"Authorization": f"Bearer {staff_token_fixture}"}
    movie_id = movie_fixture["id"]
    auditorium_id = auditorium_fixture["id"]
    response = client.post("/functions/", json={"movie_id": movie_id, "auditorium_id": auditorium_id, "start_time": "2025-09-30 15:00:00", "end_time": "2025-09-30 16:00:00", "available_seats": 100, "price": 10}, headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["movie_id"] == movie_id
    assert data["auditorium_id"] == auditorium_id

def test_create_function_unauthorized(client, movie_fixture, auditorium_fixture):
    movie_id = movie_fixture["id"]
    auditorium_id = auditorium_fixture["id"]
    response = client.post("/functions/", json={"movie_id": movie_id, "auditorium_id": auditorium_id, "start_time": "2025-09-30 15:00:00", "end_time": "2025-09-30 16:00:00", "available_seats": 100, "price": 10})
    assert response.status_code == 401

def test_create_function_forbidden(client, movie_fixture, auditorium_fixture, user_token_fixture):
    headers = {"Authorization": f"Bearer {user_token_fixture}"}
    movie_id = movie_fixture["id"]
    auditorium_id = auditorium_fixture["id"]
    response = client.post("/functions/", json={"movie_id": movie_id, "auditorium_id": auditorium_id, "start_time": "2025-09-30 15:00:00", "end_time": "2025-09-30 16:00:00", "available_seats": 100, "price": 10}, headers=headers)
    assert response.status_code == 403

def test_get_function(client, function_fixture):
    function_id = function_fixture["id"]
    response = client.get(f"/functions/{function_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == function_id

def test_get_all_functions(client, function_fixture):
    response = client.get("/functions/all")
    assert response.status_code == 200
    assert response.json()["total"] > 0

def test_create_function_movie_not_found(client, auditorium_fixture, staff_token_fixture):
    headers = {"Authorization": f"Bearer {staff_token_fixture}"}
    auditorium_id = auditorium_fixture["id"]
    response = client.post("/functions/", json={"movie_id": "non-existent-id", "auditorium_id": auditorium_id, "start_time": "2025-09-30 15:00:00", "end_time": "2025-09-30 16:00:00", "available_seats": 100, "price": 10}, headers=headers)
    assert response.status_code == 404
    assert response.json()["detail"] == "Movie not found"

def test_create_function_auditorium_not_found(client, movie_fixture, staff_token_fixture):
    headers = {"Authorization": f"Bearer {staff_token_fixture}"}
    movie_id = movie_fixture["id"]
    response = client.post("/functions/", json={"movie_id": movie_id, "auditorium_id": "non-existent-id", "start_time": "2025-09-30 15:00:00", "end_time": "2025-09-30 16:00:00", "available_seats": 100, "price": 10}, headers=headers)
    assert response.status_code == 404
    assert response.json()["detail"] == "Auditorium not found"

def test_create_function_invalid_seats(client, movie_fixture, auditorium_fixture, staff_token_fixture):
    headers = {"Authorization": f"Bearer {staff_token_fixture}"}
    movie_id = movie_fixture["id"]
    auditorium_id = auditorium_fixture["id"]
    response = client.post("/functions/", json={"movie_id": movie_id, "auditorium_id": auditorium_id, "start_time": "2025-09-30 15:00:00", "end_time": "2025-09-30 16:00:00", "available_seats": 200, "price": 10}, headers=headers)
    assert response.status_code == 400
    assert response.json()["detail"] == "Available seats cannot be greater than auditorium capacity"

def test_create_function_auditorium_not_free(client, movie_fixture, auditorium_fixture, function_fixture, staff_token_fixture):
    headers = {"Authorization": f"Bearer {staff_token_fixture}"}
    movie_id = movie_fixture["id"]
    auditorium_id = auditorium_fixture["id"]
    response = client.post("/functions/", json={"movie_id": movie_id, "auditorium_id": auditorium_id, "start_time": "2025-09-30 15:00:00", "end_time": "2025-09-30 16:00:00", "available_seats": 100, "price": 10}, headers=headers)
    assert response.status_code == 400
    assert response.json()["detail"] == "Auditorium is not free"

def test_create_function_invalid_time(client, movie_fixture, auditorium_fixture, staff_token_fixture):
    headers = {"Authorization": f"Bearer {staff_token_fixture}"}
    movie_id = movie_fixture["id"]
    auditorium_id = auditorium_fixture["id"]
    response = client.post("/functions/", json={"movie_id": movie_id, "auditorium_id": auditorium_id, "start_time": "2025-09-20 16:00:00", "end_time": "2025-09-20 15:00:00", "available_seats": 100, "price": 10}, headers=headers)
    assert response.status_code == 400
    assert response.json()["detail"] == "Start time cannot be after end time"

def test_create_function_past_time(client, movie_fixture, auditorium_fixture, staff_token_fixture):
    headers = {"Authorization": f"Bearer {staff_token_fixture}"}
    movie_id = movie_fixture["id"]
    auditorium_id = auditorium_fixture["id"]
    response = client.post("/functions/", json={"movie_id": movie_id, "auditorium_id": auditorium_id, "start_time": "2020-09-21 15:00:00", "end_time": "2020-09-21 16:00:00", "available_seats": 100, "price": 10}, headers=headers)
    assert response.status_code == 400
    assert response.json()["detail"] == "Start time cannot be in the past"

def test_get_function_not_found(client):
    response = client.get("/functions/non-existent-id")
    assert response.status_code == 404
    assert response.json()["detail"] == "Function not found"

def test_get_active_functions(client, function_fixture, staff_token_fixture):
    headers = {"Authorization": f"Bearer {staff_token_fixture}"}
    response = client.get("/functions/", headers=headers)
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_delete_function(client, function_fixture, staff_token_fixture):
    headers = {"Authorization": f"Bearer {staff_token_fixture}"}
    function_id = function_fixture["id"]
    response = client.delete(f"/functions/{function_id}", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == function_id

def test_delete_function_not_found(client, staff_token_fixture):
    headers = {"Authorization": f"Bearer {staff_token_fixture}"}
    response = client.delete("/functions/non-existent-id", headers=headers)
    assert response.status_code == 404
    assert response.json()["detail"] == "Function not found"
