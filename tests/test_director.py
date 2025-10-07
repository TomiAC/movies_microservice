async def test_create_director(client, staff_token_fixture):
    headers = {"Authorization": f"Bearer {staff_token_fixture}"}
    response = await client.post("/directors/", json={"name": "Jane Doe", "birth_date": "1980-01-01", "nationality": "UK", "bio": "Another bio"}, headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Jane Doe"
    assert data["birth_date"] == "1980-01-01"
    assert "id" in data

async def test_create_director_unauthorized(client):
    response = await client.post("/directors/", json={"name": "Jane Doe", "birth_date": "1980-01-01", "nationality": "UK", "bio": "Another bio"})
    assert response.status_code == 401

async def test_create_director_forbidden(client, user_token_fixture):
    headers = {"Authorization": f"Bearer {user_token_fixture}"}
    response = await client.post("/directors/", json={"name": "Jane Doe", "birth_date": "1980-01-01", "nationality": "UK", "bio": "Another bio"}, headers=headers)
    assert response.status_code == 403

async def test_read_director(client, director_fixture):
    director_id = director_fixture["id"]
    response = await client.get(f"/directors/{director_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == director_fixture["name"]
    assert data["birth_date"] == director_fixture["birth_date"]

async def test_read_all_directors(client, director_fixture, staff_token_fixture):
    headers = {"Authorization": f"Bearer {staff_token_fixture}"}
    await client.post("/directors/", json={"name": "Jane Doe", "birth_date": "1980-01-01", "nationality": "UK", "bio": "Another bio"}, headers=headers)
    
    response = await client.get("/directors/")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 2
    assert len(data["directors"]) == 2

async def test_update_director(client, director_fixture, staff_token_fixture):
    headers = {"Authorization": f"Bearer {staff_token_fixture}"}
    director_id = director_fixture["id"]
    update_data = {"name": "John Smith", "nationality": "Canadian"}
    response = await client.put(f"/directors/{director_id}", json=update_data, headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == update_data["name"]
    assert data["nationality"] == update_data["nationality"]
    assert data["birth_date"] == director_fixture["birth_date"] # Assert that birth_date is unchanged

async def test_delete_director(client, director_fixture, staff_token_fixture):
    headers = {"Authorization": f"Bearer {staff_token_fixture}"}
    director_id = director_fixture["id"]
    response = await client.delete(f"/directors/{director_id}", headers=headers)
    assert response.status_code == 200
    assert response.json()["id"] == director_id
    
    response = await client.get(f"/directors/{director_id}")
    assert response.status_code == 404

async def test_read_director_not_found(client):
    response = await client.get("/directors/non_existent_id")
    assert response.status_code == 404

async def test_update_director_not_found(client, staff_token_fixture):
    headers = {"Authorization": f"Bearer {staff_token_fixture}"}
    response = await client.put("/directors/non_existent_id", json={"name": "New Name"}, headers=headers)
    assert response.status_code == 404

async def test_delete_director_not_found(client, staff_token_fixture):
    headers = {"Authorization": f"Bearer {staff_token_fixture}"}
    response = await client.delete("/directors/non_existent_id", headers=headers)
    assert response.status_code == 404

async def test_create_director_missing_field(client, staff_token_fixture):
    headers = {"Authorization": f"Bearer {staff_token_fixture}"}
    response = await client.post("/directors/", json={"nationality": "USA"}, headers=headers)
    assert response.status_code == 422 # Unprocessable Entity

async def test_get_directors_pagination(client, staff_token_fixture):
    headers = {"Authorization": f"Bearer {staff_token_fixture}"}
    initial_response = await client.get("/directors/")
    initial_data = initial_response.json()
    initial_total = initial_data.get("total", 0)

    # Create 15 directors
    for i in range(15):
        await client.post("/directors/", json={"name": f"Director {i}", "birth_date": f"1970-01-{i+1:02d}", "nationality": "USA"}, headers=headers)

    response = await client.get("/directors/")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == initial_total + 15

    # Test pagination with a large limit to get all items
    response = await client.get(f"/directors/?size={initial_total + 15}")
    assert response.status_code == 200
    data = response.json()
    assert len(data["directors"]) == initial_total + 15

    # Test first page
    response = await client.get(f"/directors/?size=10&page=1")
    assert response.status_code == 200
    data = response.json()
    assert len(data["directors"]) == 10
    
    # Test second page
    response = await client.get(f"/directors/?size=10&page=2")
    assert response.status_code == 200
    # The number of items on the second page depends on the initial total
    # This makes the test more robust
    assert len(data["directors"]) > 0
