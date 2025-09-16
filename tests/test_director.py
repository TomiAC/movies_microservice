def test_create_director(client):
    response = client.post("/directors", json={"name": "John Doe", "birth_date": "1970-01-01", "nationality": "USA", "bio": "Some bio"})
    assert response.status_code == 200
    assert response.json()["name"] == "John Doe"

def test_read_director(client):
    response_new_director = client.post("/directors", json={"name": "Michael Jackson", "birth_date": "1958-08-29", "nationality": "USA", "bio": "Some bio"})
    assert response_new_director.status_code == 200
    director_id = response_new_director.json()["id"]
    response = client.get(f"/directors/{director_id}")
    assert response.status_code == 200
    assert response.json()["name"] == "Michael Jackson"

def test_read_all_directors(client):
    response_new_director = client.post("/directors", json={"name": "Michael Jackson", "birth_date": "1958-08-29", "nationality": "USA", "bio": "Some bio"})
    assert response_new_director.status_code == 200
    response = client.get("/directors")
    assert response.status_code == 200
    assert len(response.json()["directors"]) > 0

def test_update_director(client):
    response_new_director = client.post("/directors", json={"name": "Michael Jackson", "birth_date": "1958-08-29", "nationality": "USA", "bio": "Some bio"})
    assert response_new_director.status_code == 200
    new_director_id = response_new_director.json()["id"]
    response = client.put(f"/directors/{new_director_id}", json={"name": "Cristopher Nolan"})
    assert response.status_code == 200
    assert response.json()["name"] == "Cristopher Nolan"

def test_delete_director(client):
    response_new_director = client.post("/directors", json={"name": "Michael Jackson", "birth_date": "1958-08-29", "nationality": "USA", "bio": "Some bio"})
    assert response_new_director.status_code == 200
    new_director_id = response_new_director.json()["id"]
    response = client.delete(f"/directors/{new_director_id}")
    assert response.status_code == 200
    assert response.json()["id"] == new_director_id
    response = client.get(f"/directors/{new_director_id}")
    assert response.status_code == 404
    assert response.json()["detail"] == "Director not found"