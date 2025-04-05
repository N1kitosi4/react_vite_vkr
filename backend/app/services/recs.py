import string
import re
import numpy as np
from fastapi import HTTPException, status
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import TruncatedSVD
from sklearn.metrics.pairwise import cosine_similarity
from gensim.models.word2vec import Word2Vec
from sqlalchemy.orm import Session

from app.models.book import Book
from app.models.review import Review


def get_all_books(db: Session):
    return db.query(Book).all()


def get_all_reviews(db: Session):
    return db.query(Review).all()


def get_user_favorite_books(user_id: int, db: Session):
    return (
        db.query(Book)
        .join(Review.book)
        .filter(Review.user_id == user_id, Review.rating >= 4)
        .all()
    )


def process_book_genres(books):
    genres = [book.genre for book in books]
    vectorizer = TfidfVectorizer()
    genre_vectors = vectorizer.fit_transform(genres)
    # print("process_book_genres() - genre_vectors: ", genre_vectors)
    n_features = genre_vectors.shape[1]
    n_components = min(n_features - 1, 5) if n_features > 1 else 1

    lsa = TruncatedSVD(n_components=n_components)
    genre_lsa_vectors = lsa.fit_transform(genre_vectors)
    # print("process_book_genres() - genre_lsa_vectors: ", genre_lsa_vectors)
    return genre_lsa_vectors


def train_word2vec(reviews):
    inp_str = ' '.join([review.content for review in reviews])
    opt = re.sub(r'[^\w\s]', '', inp_str)
    help_list = opt.split()
    # print("train_word2vec() - help_list: ", help_list)
    tokenized_reviews = [helper for helper in help_list]
    # print("train_word2vec() - tokenized_reviews: ", tokenized_reviews)
    model = Word2Vec(sentences=tokenized_reviews, vector_size=50, window=3, min_count=1, workers=4)
    # print("train_word2vec() - model: ", model)
    return model


def clean_text(text):
    text = text.lower()
    text = re.sub(f"[{re.escape(string.punctuation)}]", "", text)
    return text


def train_word2vec(reviews):
    tokenized_reviews = [clean_text(review.content).split() for review in reviews]
    # print("train_word2vec() - tokenized_reviews: ", tokenized_reviews)
    model = Word2Vec(sentences=tokenized_reviews, vector_size=50, window=3, min_count=1, workers=4)

    return model


def get_review_vectors(books, reviews, model):
    book_review_vectors = {}

    book_reviews = {book.id: [] for book in books}
    for review in reviews:
        book_reviews[review.book_id].append(review.content)

    # print("book_reviews: ", book_reviews)
    for book_id, review_texts in book_reviews.items():
        words = ' '.join(review_texts).split()
        # print(f"get_review_vectors() - words (book_id = {book_id}): ", words)
        vectors = [model.wv[word] for word in words if word in model.wv]
        # print("get_review_vectors() - vectors: ", vectors)
        book_review_vectors[book_id] = np.mean(vectors, axis=0) if vectors else np.zeros(50)
        # print("get_review_vectors() - book_review_vector: ", vectors)
    # print("get_review_vectors() - book_reviews_vectors: ", book_review_vectors)
    return book_review_vectors


def hybrid_recommendation(user_id: int, db: Session, top_n=5):
    favorite_books = get_user_favorite_books(user_id, db)

    if not favorite_books:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT,
                            detail="You are haven't any reviews,"
                                   " add them to determine your preferences")

    all_books = get_all_books(db)
    all_reviews = get_all_reviews(db)

    genre_vectors = process_book_genres(all_books)

    word2vec_model = train_word2vec(all_reviews)
    review_vectors = get_review_vectors(all_books, all_reviews, word2vec_model)

    book_ids = [book.id for book in all_books]
    fav_book_ids = [book.id for book in favorite_books]
    fav_indices = [book_ids.index(book_id) for book_id in fav_book_ids]

    fav_genre_vectors = genre_vectors[fav_indices]
    genre_similarity_matrix = cosine_similarity(fav_genre_vectors, genre_vectors)
    avg_genre_similarity = np.mean(genre_similarity_matrix, axis=0)

    review_matrix = np.array([review_vectors[book.id] for book in all_books])
    fav_review_vectors = review_matrix[fav_indices]
    review_similarity_matrix = cosine_similarity(fav_review_vectors, review_matrix)
    avg_review_similarity = np.mean(review_similarity_matrix, axis=0)

    final_scores = 0.6 * avg_genre_similarity + 0.4 * avg_review_similarity

    recommended_indices = np.argsort(final_scores)[::-1]

    recommended_books = [
        all_books[idx] for idx in recommended_indices if all_books[idx].id not in fav_book_ids
    ]

    return recommended_books[:top_n]
