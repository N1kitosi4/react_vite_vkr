import pytest


def test_register_user(client):
    response = client.post("/users/register", json={
        "email": "testuser@example.com",
        "username": "testuser",
        "password": "securepassword"
    })
    # print(response.json())
    assert response.status_code == 201
    assert response.json()["email"] == "testuser@example.com"


def test_failed_password_register_user(client):
    response = client.post("/users/register", json={
        "email": "testuser@example.com",
        "username": "testuser",
        "password": "securepassword123"
    })

    assert response.status_code == 403


def test_failed_username_register_user(client):
    response = client.post("/users/register", json={
        "email": "testuser@example.com",
        "username": "testuser123",
        "password": "securepassword"
    })

    assert response.status_code == 403


def test_register_user2(client):
    response = client.post("/users/register", json={
        "email": "testuser2@example.com",
        "username": "testuser2",
        "password": "securepassword"
    })

    assert response.status_code == 201
    assert response.json()["email"] == "testuser2@example.com"


def test_login_user(client):
    client.post("/users/register", json={
        "email": "testlogin@example.com",
        "username": "testlogin",
        "password": "securepassword"
    })

    response = client.post("/users/login", data={
        "username": "testlogin",
        "password": "securepassword"
    })
    assert response.json()["token_type"] == "bearer"


def test_failed_username_login_user(client):
    client.post("/users/register", json={
        "email": "testlogin2@example.com",
        "username": "testlogin2",
        "password": "securepassword"
    })

    response = client.post("/users/login", data={
        "username": "testlogin123",
        "password": "securepassword"
    })
    assert response.status_code == 401


def test_failed_password_login_user(client):
    client.post("/users/register", json={
        "email": "testlogin3@example.com",
        "username": "testlogin3",
        "password": "securepassword"
    })

    response = client.post("/users/login", data={
        "username": "testlogin3",
        "password": "securepassword123"
    })
    assert response.status_code == 401


def test_get_current_user(client):
    client.post("/users/register", json={
        "email": "currentuser@example.com",
        "username": "currentuser",
        "password": "securepassword"
    })

    token_response = client.post("/users/login", data={
        "username": "currentuser",
        "password": "securepassword"
    })

    access_token = token_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {access_token}"}

    response = client.get("/users/me", headers=headers)
    assert response.status_code == 200
    assert response.json()["email"] == "currentuser@example.com"


def test_failed_get_current_user(client):
    client.post("/users/register", json={
        "email": "currentuser12345@example.com",
        "username": "currentuser12345",
        "password": "securepassword"
    })

    token_data = client.post("/users/login", data={
        "username": "currentuser12345",
        "password": "securepassword"
    })

    access_token = token_data.json()["access_token"]

    # incorrect token
    headers = {"Authorization": f"Bearer {access_token}_fail"}

    response = client.get("/users/me", headers=headers)
    assert response.status_code == 401


@pytest.mark.parametrize("email, username, password", [
    ("aha2@aha.com", "aha2", None),
    ("aha3@aha.com", None, "aha3"),
    (None, "aha4", "psw4")
])
def test_failed_create_user(client, email, username, password):
    response = client.post("/books", json={
        "title": email,
        "author": username,
        "genre": password
    })

    assert response.status_code == 422
