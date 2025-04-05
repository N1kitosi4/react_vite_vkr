import pytest


def test_create_book(client):
    response = client.post("/books", json={
        "title": "testtitle",
        "author": "testauthor",
        "genre": "testgenre",
        "img": "testimg"
    })

    assert response.status_code == 201
    assert response.json()["title"] == "testtitle"


@pytest.mark.parametrize("title, author, genre, img", [
    ("title2", "author2", None, "img2"),
    ("title3", None, "genre3", "img3"),
    (None, "author4", "genre4", "img4")
])
def test_failed_create_book(client, title, author, genre, img):
    response = client.post("/books", json={
        "title": title,
        "author": author,
        "genre": genre,
        "img": img
    })

    assert response.status_code == 422


def test_failed_copy_create_book(client):
    response = client.post("/books", json={
        "title": "testtitle",
        "author": "testauthor",
        "genre": "testgenre",
        "img": "testimg"
    })

    assert response.status_code == 422


def test_failed_nullable_create_book(client):
    response = client.post(f"/books/", json={
        "title": "",
        "author": "",
        "genre": "",
        "img": ""})
    assert response.status_code == 422


def test_get_book(client, book_id=1):
    response = client.get(f"/books/{book_id}")
    assert response.status_code == 200


@pytest.mark.parametrize("book_id", [0, -1, 1234567890])
def test_failed_int_get_book(client, book_id):
    response = client.get(f"/books/{book_id}")
    assert response.status_code == 404


@pytest.mark.parametrize("book_id", ["hello", True, None])
def test_failed_not_int_get_book(client, book_id):
    response = client.get(f"/books/{book_id}")
    assert response.status_code == 422


def test_update_book(client, book_id=1):
    response = client.put(f"/books/{book_id}", json={
        "title": "updtitle",
        "author": "updauthor",
        "genre": "updgenre",
        "img": "updimg"
    })
    assert response.status_code == 200


@pytest.mark.parametrize("book_id", [0, -1, 1234567890])
def test_failed_int_update_book(client, book_id):
    response = client.put(f"/books/{book_id}", json={
        "title": "updtitle",
        "author": "updauthor",
        "genre": "updgenre",
        "img": "updimg"})
    assert response.status_code == 404


@pytest.mark.parametrize("book_id", ["hello", True, None])
def test_failed_not_int_update_book(client, book_id):
    response = client.put(f"/books/{book_id}", json={
        "title": "updtitle",
        "author": "updauthor",
        "genre": "updgenre",
        "img": "updimg"})
    assert response.status_code == 422


def test_failed_nullable_update_book(client, book_id=1):
    response = client.put(f"/books/{book_id}", json={
        "title": "",
        "author": "",
        "genre": "",
        "img": ""})
    assert response.status_code == 422


def test_delete_book(client, book_id=1):
    response = client.delete(f"/books/{book_id}")
    assert response.status_code == 204


@pytest.mark.parametrize("book_id", [0, -1, 1234567890])
def test_failed_int_delete_book(client, book_id):
    response = client.delete(f"/books/{book_id}")
    assert response.status_code == 404


@pytest.mark.parametrize("book_id", ["hello", True, None])
def test_failed_not_int_delete_book(client, book_id):
    response = client.delete(f"/books/{book_id}")
    assert response.status_code == 422


def test_get_empty_books(client):
    client.post("")
    response = client.get("/books")
    assert response.status_code == 204


def test_get_books(client):
    client.post("/books", json={
        "title": "no_empty_title",
        "author": "no_empty_author",
        "genre": "no_empty_genre",
        "img": "no_empty_img"
    })

    response = client.get("/books")

    assert response.status_code == 200


def test_get_by_genre(client, genre="no_empty_genre2"):
    client.post("/books", json={
        "title": "no_empty_title2",
        "author": "no_empty_author2",
        "genre": "no_empty_genre2",
        "img": "no_empty_img2"
    })

    client.post("/books", json={
        "title": "no_empty_title3",
        "author": "no_empty_author3",
        "genre": "no_empty_genre2",
        "img": "no_empty_img2"
    })

    response = client.get(f"books/list_books/{genre}")
    assert len(response.json()) == 2
