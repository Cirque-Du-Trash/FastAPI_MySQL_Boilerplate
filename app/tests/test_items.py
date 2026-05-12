def test_create_item(client):
    response = client.post("/items/", json={"name": "테스트 맥북", "price": 2_000_000})
    assert response.status_code == 200

    data = response.json()
    assert data["name"] == "테스트 맥북"
    assert data["price"] == 2_000_000
    assert "id" in data


def test_read_items(client):
    response = client.get("/items/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0


def test_read_single_item(client):
    response = client.get("items/1")
    assert response.status_code == 200
    data = response.json()


def test_read_item_guard_clause(client):
    response = client.get("items/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "item not found."
