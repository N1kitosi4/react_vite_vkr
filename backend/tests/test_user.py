# import pytest
#
#
# def test_register_user(client):
#     response = client.post("/users/register", json={
#         "email": "testuser@example.com",
#         "username": "testuser",
#         "password": "securepassword"
#     })
#     # print(response.json())
#     assert response.status_code == 201
#     assert response.json()["email"] == "testuser@example.com"
#
#
# def test_failed_password_register_user(client):
#     response = client.post("/users/register", json={
#         "email": "testuser@example.com",
#         "username": "testuser",
#         "password": "securepassword123"
#     })
#
#     assert response.status_code == 403
#
#
# def test_failed_username_register_user(client):
#     response = client.post("/users/register", json={
#         "email": "testuser@example.com",
#         "username": "testuser123",
#         "password": "securepassword"
#     })
#
#     assert response.status_code == 403
#
#
# def test_register_user2(client):
#     response = client.post("/users/register", json={
#         "email": "testuser2@example.com",
#         "username": "testuser2",
#         "password": "securepassword"
#     })
#
#     assert response.status_code == 201
#     assert response.json()["email"] == "testuser2@example.com"
#
#
# def test_login_user(client):
#     client.post("/users/register", json={
#         "email": "testlogin@example.com",
#         "username": "testlogin",
#         "password": "securepassword"
#     })
#
#     response = client.post("/users/login", data={
#         "username": "testlogin",
#         "password": "securepassword"
#     })
#
#     print(response)
#     print(response.json())
#     assert response.json()["token_type"] == "bearer"
#
#
# def test_failed_username_login_user(client):
#     client.post("/users/register", json={
#         "email": "testlogin2@example.com",
#         "username": "testlogin2",
#         "password": "securepassword"
#     })
#
#     response = client.post("/users/login", data={
#         "username": "testlogin123",
#         "password": "securepassword"
#     })
#     assert response.status_code == 401
#
#
# def test_failed_password_login_user(client):
#     client.post("/users/register", json={
#         "email": "testlogin3@example.com",
#         "username": "testlogin3",
#         "password": "securepassword"
#     })
#
#     response = client.post("/users/login", data={
#         "username": "testlogin3",
#         "password": "securepassword123"
#     })
#     assert response.status_code == 401
#
#
# def test_get_current_user(client):
#     client.post("/users/register", json={
#         "email": "currentuser@example.com",
#         "username": "currentuser",
#         "password": "securepassword"
#     })
#
#     token_response = client.post("/users/login", data={
#         "username": "currentuser",
#         "password": "securepassword"
#     })
#
#     access_token = token_response.json()["access_token"]
#     headers = {"Authorization": f"Bearer {access_token}"}
#
#     response = client.get("/users/me", headers=headers)
#     assert response.status_code == 200
#     assert response.json()["email"] == "currentuser@example.com"
#
#
# def test_failed_get_current_user(client):
#     client.post("/users/register", json={
#         "email": "currentuser12345@example.com",
#         "username": "currentuser12345",
#         "password": "securepassword"
#     })
#
#     token_data = client.post("/users/login", data={
#         "username": "currentuser12345",
#         "password": "securepassword"
#     })
#
#     access_token = token_data.json()["access_token"]
#
#     # incorrect token
#     headers = {"Authorization": f"Bearer {access_token}_fail"}
#
#     response = client.get("/users/me", headers=headers)
#     assert response.status_code == 401
#
#
# @pytest.mark.parametrize("email, username, password", [
#     ("aha2@aha.com", "aha2", None),
#     ("aha3@aha.com", None, "aha3"),
#     (None, "aha4", "psw4")
# ])
# def test_failed_create_user(client, email, username, password):
#     response = client.post("/books", json={
#         "title": email,
#         "author": username,
#         "genre": password
#     })
#
#     assert response.status_code == 422


import pytest
from unittest.mock import patch
from app.models.user import User
from app.core.security import create_access_token


def test_register_user(client):
    response = client.post("/users/register", json={
        "email": "testuser@example.com",
        "username": "testuser",
        "password": "securepassword"
    })
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

    # Верифицируем пользователя
    token = create_access_token(data={"sub": "testlogin@example.com"})
    client.get(f"/users/verify-email?token={token}")

    response = client.post("/users/login", data={
        "username": "testlogin",
        "password": "securepassword"
    })
    assert response.status_code == 200
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

    # Подтверждаем email вручную через фейковый токен
    token = create_access_token(data={"sub": "currentuser@example.com"})
    client.get(f"/users/verify-email?token={token}")

    token_response = client.post("/users/login", data={
        "username": "currentuser",
        "password": "securepassword"
    })

    access_token = token_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {access_token}"}

    # Проверяем текущего пользователя
    response = client.get("/users/me", headers=headers)
    assert response.status_code == 200
    assert response.json()["email"] == "currentuser@example.com"


def test_failed_get_current_user(client):
    client.post("/users/register", json={
        "email": "currentuser12345@example.com",
        "username": "currentuser12345",
        "password": "securepassword"
    })

    # Подтверждаем email вручную через фейковый токен
    token = create_access_token(data={"sub": "currentuser12345@example.com"})
    client.get(f"/users/verify-email?token={token}")

    token_data = client.post("/users/login", data={
        "username": "currentuser12345",
        "password": "securepassword"
    })

    access_token = token_data.json()["access_token"]
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


@patch("app.routers.user.send_registration_email")
def test_register_user_sends_verification_email(mock_send_email, client, db_session):
    response = client.post("/users/register", json={
        "email": "verifyuser@example.com",
        "username": "verifyuser",
        "password": "securepassword"
    })

    assert response.status_code == 201
    mock_send_email.assert_called_once()

    user = db_session.query(User).filter_by(email="verifyuser@example.com").first()
    assert user is not None
    assert user.is_verified is False


# def test_email_verification(client, db_session):
#     email = "verifyme@example.com"
#     username = "verifyme"
#     client.post("/users/register", json={
#         "email": email,
#         "username": username,
#         "password": "securepassword"
#     })

#     token = create_access_token(data={"sub": email})
#     response = client.get(f"/users/verify-email?token={token}")

#     assert response.status_code in (200, 307)

#     user = db_session.query(User).filter_by(email=email).first()
#     assert user.is_verified is True


# def test_email_verification(client, db_session, mocker):
#     # Создаем пользователя для теста
#     email = "verifyme@example.com"
#     username = "verifyme"
#     client.post("/users/register", json={
#         "email": email,
#         "username": username,
#         "password": "securepassword"
#     })
    
#     # Создаем токен для верификации
#     token = create_access_token(data={"sub": email})

#     # Мокаем функцию верификации email
#     mock_verify_email = mocker.patch("app.routers.user.verify_email", return_value={"message": "Email successfully verified."})
    
#     # Запрашиваем верификацию email
#     response = client.get(f"/users/verify-email?token={token}")
    
#     # Проверяем, что статус ответа 200, что означает успешную обработку запроса
#     # assert response.status_code == 200
    
#     # Проверяем, что функция mock_verify_email была вызвана один раз
#     mock_verify_email.assert_called_once()
    
#     # Проверяем, что пользователь теперь верифицирован
#     user = db_session.query(User).filter_by(email=email).first()
#     assert user.is_verified is True



def test_email_verification_invalid_token(client):
    bad_token = "invalid.token.value"
    response = client.get(f"/users/verify-email?token={bad_token}")
    assert response.status_code == 400


def test_login_blocked_before_verification(client):
    client.post("/users/register", json={
        "email": "notverified@example.com",
        "username": "notverified",
        "password": "securepassword"
    })

    response = client.post("/users/login", data={
        "username": "notverified",
        "password": "securepassword"
    })

    assert response.status_code == 403
    assert "Почта не подтверждена. Проверьте входящие и спам." in response.json()["detail"]
