def test_create_genre(client):
    response = client.post("/genres/", json={"name": "Action", "description": "Action movies"})
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Action"
    assert data["description"] == "Action movies"
    assert "id" in data

def test_read_genre(client):
    response = client.post("/genres/", json={"name": "Action", "description": "Action movies"})
    assert response.status_code == 200
    genre_id = response.json()["id"]
    
    response = client.get(f"/genres/{genre_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Action"
    assert data["description"] == "Action movies"
    assert data["id"] == genre_id

def test_read_all_genres(client):
    client.post("/genres/", json={"name": "Action", "description": "Action movies"})
    client.post("/genres/", json={"name": "Comedy", "description": "Comedy movies"})
    
    response = client.get("/genres/")
    assert response.status_code == 200
    data = response.json()
    assert len(data["genres"]) == 2
    assert data["total"] == 2
    assert data["page"] == 1
    assert data["size"] == 10

def test_update_genre(client):
    response = client.post("/genres/", json={"name": "Action", "description": "Action movies"})
    assert response.status_code == 200
    genre_id = response.json()["id"]
    
    response = client.put(f"/genres/{genre_id}", json={"name": "Adventure"})
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Adventure"
    assert data["description"] == "Action movies" 

def test_delete_genre(client):
    response = client.post("/genres/", json={"name": "Action", "description": "Action movies"})
    assert response.status_code == 200
    genre_id = response.json()["id"]
    
    response = client.delete(f"/genres/{genre_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == genre_id
    
    response = client.get(f"/genres/{genre_id}")
    assert response.status_code == 404

def test_read_genre_not_found(client):
    response = client.get("/genres/non_existent_id")
    assert response.status_code == 404

def test_update_genre_not_found(client):
    response = client.put("/genres/non_existent_id", json={"name": "Adventure"})
    assert response.status_code == 404

def test_delete_genre_not_found(client):
    response = client.delete("/genres/non_existent_id")
    assert response.status_code == 404
