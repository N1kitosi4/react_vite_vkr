def test_create_review(client):
    client.post("/users/register", json={
        "email": "reviewuser@example.com",
        "username": "reviewuser",
        "password": "securepassword"
    })
    login_response = client.post("/users/login", data={
        "username": "reviewuser",
        "password": "securepassword"
    })
    # print(login_response.json())
    access_token = login_response.json()["access_token"]
    # print(access_token)
    headers = {"Authorization": f"Bearer {access_token}"}
    # print(headers)
    book_info = client.post("/books", json={
        "title": "test_title",
        "author": "test_author",
        "genre": "test_genre",
        "img": "test_img"
    })
    # print(book_info.json())
    response = client.post("/reviews", json={
        "book_title": book_info.json()["title"],
        "book_author": book_info.json()["author"],
        "rating": 5,
        "content": "Nice book"
    }, headers=headers)
    # print(response.json())

    assert response.status_code == 201
    assert response.json()["content"] == "Nice book"


def test_read_reviews(client):
    client.post("/users/register", json={
        "email": "reviewuser@example.com",
        "username": "reviewuser",
        "password": "securepassword"
    })
    login_response = client.post("/users/login", data={
        "username": "reviewuser",
        "password": "securepassword"
    })
    # print(login_response.json())
    access_token = login_response.json()["access_token"]
    # print(access_token)
    headers = {"Authorization": f"Bearer {access_token}"}
    # print(headers)
    response = client.get("/books")
    print(response.json())
    assert len(response.json()) == 4
    assert response.status_code == 200


def test_update_review(client):
    client.post("/users/register", json={
        "email": "updatereview@example.com",
        "username": "updatereview",
        "password": "securepassword"
    })
    login_response = client.post("/users/login", data={
        "username": "updatereview",
        "password": "securepassword"
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
    client.post("/users/register", json={
        "email": "deletereview@example.com",
        "username": "deletereview",
        "password": "securepassword"
    })
    login_response = client.post("/users/login", data={
        "username": "deletereview",
        "password": "securepassword"
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
