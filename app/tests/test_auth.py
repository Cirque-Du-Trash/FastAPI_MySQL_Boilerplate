def test_register(client):
    response = client.post(
        "/users/register", json={"username": "newuser", "password": "newpass123"}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["username"] == "newuser"
    assert data["is_superuser"] is False


def test_register_duplicate(client):
    client.post(
        "/users/register", json={"username": "dupeuser", "password": "pass123456"}
    )
    response = client.post(
        "/users/register", json={"username": "dupeuser", "password": "pass123456"}
    )
    assert response.status_code == 409


def test_login(client):
    client.post(
        "/users/register", json={"username": "loginuser", "password": "loginpass1"}
    )
    response = client.post(
        "/auth/login", data={"username": "loginuser", "password": "loginpass1"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert "refresh_token" in data
    assert data["token_type"] == "bearer"


def test_login_wrong_password(client):
    response = client.post(
        "/auth/login", data={"username": "loginuser", "password": "wrongpass1"}
    )
    assert response.status_code == 401


def test_refresh_token(client):
    client.post(
        "/users/register", json={"username": "refreshuser", "password": "refpass123"}
    )
    login = client.post(
        "/auth/login", data={"username": "refreshuser", "password": "refpass123"}
    )
    refresh_token = login.json()["refresh_token"]
    response = client.post(f"/auth/refresh?refresh_token={refresh_token}")
    assert response.status_code == 200
    assert "access_token" in response.json()


def test_logout(client):
    client.post(
        "/users/register", json={"username": "logoutuser", "password": "logout1234"}
    )
    login = client.post(
        "/auth/login", data={"username": "logoutuser", "password": "logout1234"}
    )
    token = login.json()["access_token"]
    response = client.post("/auth/logout", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert response.json()["detail"] == "Successfully logged out"
