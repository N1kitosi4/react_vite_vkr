# from fastapi.testclient import TestClient
# from app.main import app
#
# client = TestClient(app)
#
#
# def test_recommendations_ml():
#     """
#     Проверяем, что ML-рекомендации работают корректно.
#     """
#     # 1. Регистрируем нового пользователя
#     user_data = {"username": "testuser_ml", "email": "test_ml@example.com", "password": "testpassword"}
#     register_response = client.post("/users/register", json=user_data)
#     assert register_response.status_code == 201
#     user = register_response.json()
#
#     # 2. Логинимся и получаем access_token
#     login_response = client.post("/users/login", data={"username": user_data["username"], "password": user_data["password"]})
#     assert login_response.status_code == 200
#     token = login_response.json()["access_token"]
#     headers = {"Authorization": f"Bearer {token}"}
#
#     # 3. Добавляем книги с разными жанрами
#     books = [
#         {"title": "Киберпанк 1", "author": "Автор 1", "genre": "Киберпанк"},
#         {"title": "Киберпанк 2", "author": "Автор 2", "genre": "Киберпанк"},
#         {"title": "Фэнтези 1", "author": "Автор 3", "genre": "Фэнтези"},
#         {"title": "Фэнтези 2", "author": "Автор 4", "genre": "Фэнтези"},
#     ]
#
#     for book in books:
#         book_response = client.post("/books", json=book, headers=headers)
#         assert book_response.status_code == 201
#
#     # 4. Оставляем положительный отзыв на "Киберпанк 1"
#     review_response = client.post(
#         "/reviews/",
#         json={"content": "Nice book!", "rating": 5, "book_id": 1},
#         headers=headers
#     )
#     assert review_response.status_code == 201
#
#     # 5. Запрашиваем рекомендации
#     recommendations_response = client.get("/recommendations_ml", headers=headers)
#     assert recommendations_response.status_code == 200
#     recommended_books = recommendations_response.json()
#
#     # 6. Проверяем, что "Киберпанк 2" был рекомендован
#     assert any(book["title"] == "Киберпанк 2" for book in recommended_books)
#
#     print("Тест ML-рекомендаций успешно пройден!")
