from uuid import uuid4

def test_create_auditorium(client, cinema_fixture, admin_token_fixture):
    """Test the creation of a new auditorium."""
    cinema_id = cinema_fixture["id"]
    headers = {"Authorization": f"Bearer {admin_token_fixture}"}
    response = client.post(f"/auditoriums/", json={"name": "2B", "cinema_id": cinema_id, "capacity": 150}, headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "2B"
    assert data["cinema_id"] == cinema_id
    assert data["capacity"] == 150

def test_create_auditorium_unauthorized(client, cinema_fixture):
    """Test the creation of a new auditorium without a token."""
    cinema_id = cinema_fixture["id"]
    response = client.post(f"/auditoriums/", json={"name": "2B", "cinema_id": cinema_id, "capacity": 150})
    assert response.status_code == 401

def test_create_auditorium_forbidden(client, cinema_fixture, staff_token_fixture):
    """Test the creation of a new auditorium with a non-admin token."""
    cinema_id = cinema_fixture["id"]
    headers = {"Authorization": f"Bearer {staff_token_fixture}"}
    response = client.post(f"/auditoriums/", json={"name": "2B", "cinema_id": cinema_id, "capacity": 150}, headers=headers)
    assert response.status_code == 403

def test_get_auditorium(client, auditorium_fixture):
    """Test retrieving a single auditorium by its ID."""
    auditorium_id = auditorium_fixture["id"]
    response = client.get(f"/auditoriums/{auditorium_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == auditorium_id
    assert data["name"] == auditorium_fixture["name"]
    assert data["capacity"] == auditorium_fixture["capacity"]

def test_get_auditorium_not_found(client):
    """Test retrieving a non-existent auditorium."""
    non_existent_id = str(uuid4())
    response = client.get(f"/auditoriums/{non_existent_id}")
    assert response.status_code == 404
    assert response.json()["detail"] == "Auditorium not found"

def test_get_all_auditoriums(client, cinema_fixture, admin_token_fixture):
    """Test retrieving all auditoriums for a given cinema."""
    cinema_id = cinema_fixture["id"]
    headers = {"Authorization": f"Bearer {admin_token_fixture}"}
    # Create a few auditoriums for the cinema
    client.post("/auditoriums/", json={"name": "Aud1", "cinema_id": cinema_id, "capacity": 50}, headers=headers)
    client.post("/auditoriums/", json={"name": "Aud2", "cinema_id": cinema_id, "capacity": 75}, headers=headers)
    client.post("/auditoriums/", json={"name": "Aud3", "cinema_id": cinema_id, "capacity": 120}, headers=headers)

    response = client.get(f"/auditoriums")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data["auditoriums"], list)
    # The cinema_fixture creates one auditorium, and we create 3 more
    assert data["total"] == 3
    names = {aud["name"] for aud in data["auditoriums"]}
    capacities = {aud["capacity"] for aud in data["auditoriums"]}
    assert "Aud1" in names
    assert "Aud2" in names
    assert "Aud3" in names
    assert 50 in capacities
    assert 75 in capacities
    assert 120 in capacities

def test_update_auditorium(client, auditorium_fixture, admin_token_fixture):
    """Test updating an auditorium."""
    auditorium_id = auditorium_fixture["id"]
    headers = {"Authorization": f"Bearer {admin_token_fixture}"}
    response = client.put(f"/auditoriums/{auditorium_id}", json={"name": "Updated Name"}, headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Updated Name"

def test_delete_auditorium(client, auditorium_fixture, admin_token_fixture):
    """Test deleting an auditorium."""
    auditorium_id = auditorium_fixture["id"]
    headers = {"Authorization": f"Bearer {admin_token_fixture}"}
    response = client.delete(f"/auditoriums/{auditorium_id}", headers=headers)
    assert response.status_code == 200
    # Verify that the auditorium is deleted
    response = client.get(f"/auditoriums/{auditorium_id}")
    assert response.status_code == 404


