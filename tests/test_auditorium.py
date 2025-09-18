from uuid import uuid4

def test_create_auditorium(client, cinema_fixture):
    """Test the creation of a new auditorium."""
    cinema_id = cinema_fixture["id"]
    response = client.post(f"/auditoriums/", json={"name": "2B", "cinema_id": cinema_id, "capacity": 150})
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "2B"
    assert data["cinema_id"] == cinema_id
    assert data["capacity"] == 150

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

def test_get_all_auditoriums(client, cinema_fixture):
    """Test retrieving all auditoriums for a given cinema."""
    cinema_id = cinema_fixture["id"]
    # Create a few auditoriums for the cinema
    client.post("/auditoriums/", json={"name": "Aud1", "cinema_id": cinema_id, "capacity": 50})
    client.post("/auditoriums/", json={"name": "Aud2", "cinema_id": cinema_id, "capacity": 75})
    client.post("/auditoriums/", json={"name": "Aud3", "cinema_id": cinema_id, "capacity": 120})

    response = client.get(f"/auditoriums")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data["auditoriums"], list)
    assert len(data) == 4
    # Check if the names and capacities are as expected (order might vary)
    names = {aud["name"] for aud in data["auditoriums"]}
    capacities = {aud["capacity"] for aud in data["auditoriums"]}
    assert "Aud1" in names
    assert "Aud2" in names
    assert "Aud3" in names
    assert 50 in capacities
    assert 75 in capacities
    assert 120 in capacities


