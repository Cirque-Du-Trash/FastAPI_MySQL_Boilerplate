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
    create_response = client.post(
        "/items/", json={"name": "단일 조회 테스트용", "price": 5000}
    )
    item_id = create_response.json()["id"]

    response = client.get(f"/items/{item_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "단일 조회 테스트용"


def test_read_item_guard_clause(client):
    response = client.get("items/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "item not found."


def test_create_item_negative_price(client):
    response = client.post("/items/", json={"name": "음수폰", "price": -100})
    assert response.status_code == 422


def test_create_item_invalid_type(client):
    response = client.post("/items/", json={"name": "공짜폰", "price": "공짜"})
    assert response.status_code == 422


def test_read_items_with_min_price(client):
    response = client.get("/items/?min_price=9999999999")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 0


def test_read_item_empty_name(client):
    response = client.post("/items/", json={"name": "", "price": 1000})
    assert response.status_code == 422


def test_create_item_long_name(client):
    response = client.post("/items/", json={"name": "a" * 256, "price": 1000})
    assert response.status_code == 422


def test_read_items_invalid_limit(client):
    response = client.get("/items/?limit=1000")
    assert response.status_code == 422
