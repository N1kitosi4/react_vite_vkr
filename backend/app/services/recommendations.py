import numpy as np
from fastapi import HTTPException, status
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sqlalchemy.orm import Session
from app.models.book import Book
from app.models.review import Review


def get_all_books(db: Session):
    return db.query(Book).all()


def get_user_favourite_books(user_id: int, db: Session):
    favourite_books = (
        db.query(Book)
        .join(Review.book)
        .filter(Review.user_id == user_id, Review.rating >= 4)
        .all()
    )
    return favourite_books


def recommend_books_ml(user_id: int, db: Session, top_n=5):
    favorite_books = get_user_favourite_books(user_id, db)

    if not favorite_books:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT)
        # return []

    all_books = get_all_books(db)

    # Создаём словарь {id книги: жанр}
    book_dict_genres = {book.id: book.genre for book in all_books}

    # Формируем список жанров книг, векторизуем через TF-IDF
    book_ids, book_genres = zip(*book_dict_genres.items())
    vectorizer = TfidfVectorizer()
    book_vectors = vectorizer.fit_transform(book_genres)

    # Определяем векторы любимых книг пользователя
    fav_book_ids = [book.id for book in favorite_books]
    fav_indices = [book_ids.index(book_id) for book_id in fav_book_ids]
    fav_vectors = book_vectors[fav_indices]

    # Считаем косинусное сходство между любимыми книгами и всеми книгами
    similarity_matrix = cosine_similarity(fav_vectors, book_vectors)

    # Получаем среднее сходство по всем любимым книгам
    avg_similarity = np.mean(similarity_matrix, axis=0)

    # Находим книги с наибольшим сходством
    recommended_indices = np.argsort(avg_similarity)[::-1]

    # Фильтруем уже прочитанные книги
    recommended_books = [
        all_books[idx] for idx in recommended_indices if all_books[idx].id not in fav_book_ids
    ]

    return recommended_books[:top_n]
