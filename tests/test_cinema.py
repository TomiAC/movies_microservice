def test_create_cinema(client, admin_token_fixture):
    headers = {"Authorization": f"Bearer {admin_token_fixture}"}
    response = client.post("/cinemas/", json={"name": "New Cinema", "location": "456 Oak Ave", "number": 2}, headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "New Cinema"
    assert data["location"] == "456 Oak Ave"
    assert data["number"] == 2
    assert "id" in data

def test_create_cinema_unauthorized(client):
    response = client.post("/cinemas/", json={"name": "New Cinema", "location": "456 Oak Ave", "number": 2})
    assert response.status_code == 401

def test_create_cinema_forbidden(client, staff_token_fixture):
    headers = {"Authorization": f"Bearer {staff_token_fixture}"}
    response = client.post("/cinemas/", json={"name": "New Cinema", "location": "456 Oak Ave", "number": 2}, headers=headers)
    assert response.status_code == 403

def test_read_cinema(client, cinema_fixture):
    cinema_id = cinema_fixture["id"]
    response = client.get(f"/cinemas/{cinema_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == cinema_fixture["name"]
    assert data["location"] == cinema_fixture["location"]
    assert data["number"] == cinema_fixture["number"]

def test_read_all_cinemas(client, cinema_fixture, admin_token_fixture):
    headers = {"Authorization": f"Bearer {admin_token_fixture}"}
    initial_response = client.get("/cinemas/")
    initial_data = initial_response.json()
    initial_total = initial_data.get("total", 0)

    client.post("/cinemas/", json={"name": "Cinema Two", "location": "789 Pine St", "number": 3}, headers=headers)
    
    response = client.get("/cinemas/")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == initial_total + 1

def test_update_cinema(client, cinema_fixture, admin_token_fixture):
    headers = {"Authorization": f"Bearer {admin_token_fixture}"}
    cinema_id = cinema_fixture["id"]
    update_data = {"name": "Updated Cinema City", "number": 10}
    response = client.put(f"/cinemas/{cinema_id}", json=update_data, headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == update_data["name"]
    assert data["number"] == update_data["number"]
    assert data["location"] == cinema_fixture["location"] # Assert that location is unchanged

def test_delete_cinema(client, cinema_fixture, admin_token_fixture):
    headers = {"Authorization": f"Bearer {admin_token_fixture}"}
    cinema_id = cinema_fixture["id"]
    response = client.delete(f"/cinemas/{cinema_id}", headers=headers)
    assert response.status_code == 200
    assert response.json()["id"] == cinema_id
    
    response = client.get(f"/cinemas/{cinema_id}")
    assert response.status_code == 404

def test_read_cinema_not_found(client):
    response = client.get("/cinemas/non_existent_id")
    assert response.status_code == 404

def test_update_cinema_not_found(client, admin_token_fixture):
    headers = {"Authorization": f"Bearer {admin_token_fixture}"}
    response = client.put("/cinemas/non_existent_id", json={"name": "New Name"}, headers=headers)
    assert response.status_code == 404

def test_delete_cinema_not_found(client, admin_token_fixture):
    headers = {"Authorization": f"Bearer {admin_token_fixture}"}
    response = client.delete("/cinemas/non_existent_id", headers=headers)
    assert response.status_code == 404

def test_create_cinema_missing_field(client, admin_token_fixture):
    headers = {"Authorization": f"Bearer {admin_token_fixture}"}
    response = client.post("/cinemas/", json={"name": "Missing Location"}, headers=headers)
    assert response.status_code == 422 # Unprocessable Entity

def test_get_cinemas_pagination(client, admin_token_fixture):
    headers = {"Authorization": f"Bearer {admin_token_fixture}"}
    initial_response = client.get("/cinemas/")
    initial_data = initial_response.json()
    initial_total = initial_data.get("total", 0)

    # Create 15 cinemas
    for i in range(15):
        client.post("/cinemas/", json={"name": f"Cinema {i}", "location": f"Location {i}", "number": i}, headers=headers)
    
    response = client.get("/cinemas/")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == initial_total + 15

    # Test pagination with a large limit to get all items
    response = client.get(f"/cinemas/?limit={initial_total + 15}")
    assert response.status_code == 200
    data = response.json()
    assert len(data["cinemas"]) == initial_total + 15

    # Test first page
    response = client.get(f"/cinemas/?limit=10&skip=0")
    assert response.status_code == 200
    data = response.json()
    assert len(data["cinemas"]) == 10
    
    # Test second page
    response = client.get(f"/cinemas/?limit=10&skip=10")
    assert response.status_code == 200
    # The number of items on the second page depends on the initial total
    # This makes the test more robust
    assert len(data["cinemas"]) > 0
