def test_create_genre(client, staff_token_fixture):
    headers = {"Authorization": f"Bearer {staff_token_fixture}"}
    response = client.post("/genres/", json={"name": "Comedy", "description": "Comedy movies"}, headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Comedy"
    assert data["description"] == "Comedy movies"
    assert "id" in data

def test_create_genre_unauthorized(client):
    response = client.post("/genres/", json={"name": "Comedy", "description": "Comedy movies"})
    assert response.status_code == 401

def test_create_genre_forbidden(client, user_token_fixture):
    headers = {"Authorization": f"Bearer {user_token_fixture}"}
    response = client.post("/genres/", json={"name": "Comedy", "description": "Comedy movies"}, headers=headers)
    assert response.status_code == 403

def test_read_genre(client, genre_fixture):
    genre_id = genre_fixture["id"]
    
    response = client.get(f"/genres/{genre_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["name"].startswith("Action")
    assert data["description"] == "Action movies"
    assert data["id"] == genre_id

def test_read_all_genres(client, genre_fixture, staff_token_fixture):
    headers = {"Authorization": f"Bearer {staff_token_fixture}"}
    client.post("/genres/", json={"name": "Comedy", "description": "Comedy movies"}, headers=headers)
    
    response = client.get("/genres/")
    assert response.status_code == 200
    data = response.json()
    assert len(data["genres"]) == 2
    assert data["total"] == 2
    assert data["page"] == 1
    assert data["size"] == 10

def test_update_genre(client, genre_fixture, staff_token_fixture):
    headers = {"Authorization": f"Bearer {staff_token_fixture}"}
    genre_id = genre_fixture["id"]
    
    response = client.put(f"/genres/{genre_id}", json={"name": "Adventure"}, headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Adventure"
    assert data["description"] == "Action movies" 

def test_delete_genre(client, genre_fixture, staff_token_fixture):
    headers = {"Authorization": f"Bearer {staff_token_fixture}"}
    genre_id = genre_fixture["id"]
    
    response = client.delete(f"/genres/{genre_id}", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == genre_id
    
    response = client.get(f"/genres/{genre_id}")
    assert response.status_code == 404

def test_read_genre_not_found(client):
    response = client.get("/genres/non_existent_id")
    assert response.status_code == 404

def test_update_genre_not_found(client, staff_token_fixture):
    headers = {"Authorization": f"Bearer {staff_token_fixture}"}
    response = client.put("/genres/non_existent_id", json={"name": "Adventure"}, headers=headers)
    assert response.status_code == 404

def test_delete_genre_not_found(client, staff_token_fixture):
    headers = {"Authorization": f"Bearer {staff_token_fixture}"}
    response = client.delete("/genres/non_existent_id", headers=headers)
    assert response.status_code == 404
