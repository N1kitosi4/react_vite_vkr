from app.core.security import create_access_token


def test_create_review(client):
    email = "reviewuser@example.com"
    username = "reviewuser"
    password = "securepassword"

    client.post("/users/register", json={
        "email": email,
        "username": username,
        "password": password
    })

    # Подтверждаем email
    token = create_access_token(data={"sub": email})
    client.get(f"/users/verify-email?token={token}")

    login_response = client.post("/users/login", data={
        "username": username,
        "password": password
    })

    assert login_response.status_code == 200
    access_token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {access_token}"}

    book_info = client.post("/books", json={
        "title": "test_title",
        "author": "test_author",
        "genre": "test_genre",
        "img": "test_img"
    })

    response = client.post("/reviews", json={
        "book_title": book_info.json()["title"],
        "book_author": book_info.json()["author"],
        "rating": 5,
        "content": "Nice book"
    }, headers=headers)

    assert response.status_code == 201
    assert response.json()["content"] == "Nice book"


def test_read_reviews(client):
    email = "reviewuser@example.com"
    username = "reviewuser"
    password = "securepassword"

    client.post("/users/register", json={
        "email": email,
        "username": username,
        "password": password
    })

    token = create_access_token(data={"sub": email})
    client.get(f"/users/verify-email?token={token}")

    login_response = client.post("/users/login", data={
        "username": username,
        "password": password
    })

    access_token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {access_token}"}

    response = client.get("/books", headers=headers)

    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_update_review(client):
    email = "updatereview@example.com"
    username = "updatereview"
    password = "securepassword"

    client.post("/users/register", json={
        "email": email,
        "username": username,
        "password": password
    })

    token = create_access_token(data={"sub": email})
    client.get(f"/users/verify-email?token={token}")

    login_response = client.post("/users/login", data={
        "username": username,
        "password": password
    })

    access_token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {access_token}"}

    book_info = client.post("/books", json={
        "title": "test_title2",
        "author": "test_author2",
        "genre": "test_genre2",
        "img": "test_img_2"
    })

    create_response = client.post("/reviews", json={
        "book_title": book_info.json()["title"],
        "book_author": book_info.json()["author"],
        "rating": 4,
        "content": "Good book"
    }, headers=headers)

    review_id = create_response.json()["id"]

    response = client.put(f"/reviews/{review_id}", json={
        "book_id": book_info.json()["id"],
        "rating": 5,
        "content": "test_upd_book",
        "book_title": "test_upd_book_title",
        "book_author": "test_upd_book_author",
        "book_img": "test_upd_book_img",
        "username": "test_upd_username",
        "genre": "test_upd_genre"
    }, headers=headers)

    assert response.status_code == 200
    assert response.json()["content"] == "test_upd_book"


def test_delete_review(client):
    email = "deletereview@example.com"
    username = "deletereview"
    password = "securepassword"

    client.post("/users/register", json={
        "email": email,
        "username": username,
        "password": password
    })

    token = create_access_token(data={"sub": email})
    client.get(f"/users/verify-email?token={token}")

    login_response = client.post("/users/login", data={
        "username": username,
        "password": password
    })

    access_token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {access_token}"}

    book_info = client.post("/books", json={
        "title": "test_title3",
        "author": "test_author3",
        "genre": "test_genre3"
    })

    create_response = client.post("/reviews", json={
        "book_title": book_info.json()["title"],
        "book_author": book_info.json()["author"],
        "rating": 4,
        "content": "Interesting"
    }, headers=headers)

    review_id = create_response.json()["id"]

    response = client.delete(f"/reviews/{review_id}", headers=headers)

    assert response.status_code == 204
