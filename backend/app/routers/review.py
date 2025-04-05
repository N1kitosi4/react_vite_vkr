from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status, Query

from sqlalchemy import desc, asc, func
from sqlalchemy.orm import Session

from app.models.review import Review, ReviewRating
from app.models.book import Book
from app.models.user import User

from app.schemas.review import (ReviewCreate, ReviewUpdate, ReviewResponse,
                                ReviewsWithPaginationResponse,
                                ReviewRatingCreate, ReviewRatingResponse)
from app.db.database import get_db
from app.routers.user import get_current_user


router = APIRouter()


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=ReviewResponse)
def create_review(
        review: ReviewCreate,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user),
):
    book = db.query(Book).filter(Book.title == review.book_title,
                                 Book.author == review.book_author).first()

    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")

    new_review = Review(
        content=review.content,
        rating=review.rating,
        book_id=book.id,
        user_id=current_user.id
    )

    db.add(new_review)
    db.commit()
    db.refresh(new_review)

    return {
        "id": new_review.id,
        "content": new_review.content,
        "rating": new_review.rating,
        "book_img": book.img,
        "book_title": book.title,
        "book_author": book.author,
        "genre": book.genre,
        "username": current_user.username,
        "created_at": new_review.created_at,
    }


@router.get("/", response_model=dict)  # Теперь возвращаем объект с мета-данными
def get_reviews(skip: Optional[int] = 0, limit: Optional[int] = 15, db: Session = Depends(get_db)):
    total_reviews = db.query(Review).count()  # Подсчет всех отзывов

    reviews = (db.query(Review).join(Book).join(User)
               .order_by(Review.created_at.desc())
               .offset(skip).limit(limit)
               .all())

    if not reviews:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail="No reviews found")

    return {
        "total": total_reviews,
        "skip": skip,
        "limit": limit,
        "reviews": [{
            "id": review.id,
            "content": review.content,
            "rating": review.rating,
            "book_title": review.book.title,
            "book_author": review.book.author,
            "book_img": review.book.img,
            "username": review.user.username,
            "created_at": review.created_at,
            "genre": review.book.genre
        } for review in reviews]
    }


@router.get("/profile_stats", response_model=dict)
def get_profile_stats(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    # Количество отзывов, написанных пользователем
    user_reviews_count = db.query(Review).filter(Review.user_id == current_user.id).count()

    # Средний рейтинг собственных отзывов
    user_reviews_avg_rating = db.query(func.avg(Review.rating)).filter(Review.user_id == current_user.id).scalar()
    user_reviews_avg_rating = round(user_reviews_avg_rating, 2) if user_reviews_avg_rating else 0

    # Количество оцененных пользователем отзывов других пользователей
    rated_reviews_count = db.query(ReviewRating).filter(ReviewRating.user_id == current_user.id).count()

    # Средний балл, который пользователь поставил другим отзывам
    rated_reviews_avg_rating = db.query(func.avg(ReviewRating.rating)).filter(
        ReviewRating.user_id == current_user.id).scalar()
    rated_reviews_avg_rating = round(rated_reviews_avg_rating, 2) if rated_reviews_avg_rating else 0

    return {
        "user_reviews_count": user_reviews_count,
        "user_reviews_avg_rating": user_reviews_avg_rating,
        "rated_reviews_count": rated_reviews_count,
        "rated_reviews_avg_rating": rated_reviews_avg_rating
    }


@router.get("/genres/{genre}", response_model=list[ReviewResponse])
def get_genres_reviews(genre: str, skip: Optional[int] = 0, limit: Optional[int] = 15, db: Session = Depends(get_db)):
    reviews = (db.query(Review).join(Book).join(User).filter(Book.genre == genre).
               order_by(Review.created_at.desc()).offset(skip).limit(limit).all())

    if not reviews:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT,
                            detail="No reviews found for this genre")

    return [{
        "id": review.id,
        "content": review.content,
        "rating": review.rating,
        "book_title": review.book.title,
        "book_author": review.book.author,
        "book_img": review.book.img,
        "username": review.user.username,
        "created_at": review.created_at,
        "genre": review.book.genre
    } for review in reviews]


@router.get("/review/{review_id}", response_model=ReviewResponse)
def get_review(review_id: int, db: Session = Depends(get_db)):
    review = db.query(Review).filter(Review.id == review_id).first()
    if not review:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Review not found")

    book = review.book

    return {
        "id": review.id,
        "content": review.content,
        "rating": review.rating,
        "book_img": book.img,
        "book_title": book.title,
        "genre": book.genre,
        "book_author": book.author,
        "username": review.user.username,
        "created_at": review.created_at,
    }


@router.get("/my_reviews", response_model=list[ReviewResponse])
def get_my_reviews(skip: int = 0, limit: Optional[int] = 15, db: Session = Depends(get_db),
                   current_user: User = Depends(get_current_user)):
    reviews = (db.query(Review).join(Book).join(User).filter(Review.user_id == current_user.id).
               order_by(Review.created_at.desc()).offset(skip).limit(limit).all())

    if not reviews:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT,
                            detail="No reviews found for this user")

    return [{
        "id": review.id,
        "content": review.content,
        "rating": review.rating,
        "book_title": review.book.title,
        "book_author": review.book.author,
        "book_img": review.book.img,
        "username": review.user.username,
        "created_at": review.created_at,
        "genre": review.book.genre
    } for review in reviews]


@router.get("/reviews/search", response_model=list[dict])
def search_reviews(
        genre: Optional[str] = Query(None, description="Фильтр по жанру"),
        query: Optional[str] = Query(None, description="Поиск по названию или автору"),
        rating: Optional[int] = Query(None, description="Фильтр по рейтингу"),
        sort: Optional[str] = Query("date", description="Сортировка: date, popularity, rating"),
        skip: Optional[int] = 0,
        limit: Optional[int] = 15,
        db: Session = Depends(get_db),
):
    reviews_query = db.query(Review).join(Book).join(User)

    if genre:
        reviews_query = reviews_query.filter(Book.genre.ilike(f"%{genre}%"))

    if query:
        reviews_query = reviews_query.filter(
            (Book.title.ilike(f"%{query.lower()}%")) | (Book.author.ilike(f"%{query.lower()}%"))
        )

    if rating:
        reviews_query = reviews_query.filter(Review.rating == rating)

    if sort == "date":
        reviews_query = reviews_query.order_by(desc(Review.created_at))
    elif sort == "popularity":
        reviews_query = reviews_query.join(Book).order_by(desc(Review.average_review_rating))  # Сортировка по популярности
    elif sort == "rating":
        reviews_query = reviews_query.order_by(desc(Review.rating))

    reviews = reviews_query.offset(skip).limit(limit).all()

    if not reviews:
        raise HTTPException(status_code=404, detail="Ничего не найдено")


    return [{
        "id": review.id,
        "content": review.content,
        "rating": review.rating,
        "book_title": review.book.title,
        "book_author": review.book.author,
        "book_img": review.book.img,
        "username": review.user.username,
        "created_at": review.created_at,
        "genre": review.book.genre,
        "average_review_rating": review.average_review_rating  # Добавляем средний рейтинг
    } for review in reviews]


@router.get("/reviews", response_model=list[ReviewResponse])
def get_reviews(
    genre: Optional[str] = Query(None, description="Фильтр по жанру"),
    query: Optional[str] = Query(None, description="Поиск по названию или автору"),
    rating: Optional[float] = Query(None, description="Фильтр по рейтингу"),
    sort: Optional[str] = Query("date", description="Сортировка: date, popularity, rating"),
    skip: Optional[int] = 0,
    limit: Optional[int] = 15,
    db: Session = Depends(get_db),
):
    reviews_query = db.query(Review).join(Book)

    if genre:
        reviews_query = reviews_query.filter(Book.genre.ilike(f"%{genre}%"))

    if query:
        reviews_query = reviews_query.filter(
            (Book.title.ilike(f"%{query.lower()}%")) | (Book.author.ilike(f"%{query.lower()}%"))
        )

    if rating:
        reviews_query = reviews_query.filter(Review.rating == rating)

    # Вычисление популярности на основе рейтинга от других пользователей
    if sort == "date":
        reviews_query = reviews_query.order_by(desc(Review.created_at))
    elif sort == "popularity":
        # Вычисление среднего рейтинга для отзыва
        reviews_query = reviews_query.join(ReviewRating).group_by(Review.id).order_by(
            func.avg(ReviewRating.rating).desc()
        )
    elif sort == "rating":
        reviews_query = reviews_query.order_by(desc(Review.rating))

    reviews = reviews_query.offset(skip).limit(limit).all()

    if not reviews:
        raise HTTPException(status_code=404, detail="No reviews found")

    # Вычисление среднего рейтинга для каждого отзыва
    reviews_response = []
    for review in reviews:
        # Получаем все оценки для отзыва
        ratings = db.query(ReviewRating).filter(ReviewRating.review_id == review.id).all()
        average_rating = sum(rating.rating for rating in ratings) / len(ratings) if ratings else 0

        reviews_response.append({
            "id": review.id,
            "content": review.content,
            "rating": review.rating,
            "book_title": review.book.title,
            "book_author": review.book.author,
            "book_img": review.book.img,
            "username": review.user.username,
            "created_at": review.created_at,
            "genre": review.book.genre,
            "average_review_rating": average_rating
        })

    return reviews_response


@router.get("/search_reviews", response_model=ReviewsWithPaginationResponse)
def search_get_reviews(
    genre: Optional[str] = Query(None, description="Фильтр по жанру"),
    query: Optional[str] = Query(None, description="Поиск по названию или автору"),
    rating: Optional[float] = Query(None, description="Фильтр по рейтингу"),
    sort: Optional[str] = Query("date", description="Сортировка: date, popularity, rating"),
    direction: Optional[str] = Query("desc", description="Направление сортировки: asc или desc"),
    skip: Optional[int] = 0,
    limit: Optional[int] = 15,
    db: Session = Depends(get_db),
):
    reviews_query = db.query(Review).join(Book)

    if genre:
        reviews_query = reviews_query.filter(Book.genre.ilike(f"%{genre}%"))

    if query:
        reviews_query = reviews_query.filter(
            (Book.title.ilike(f"%{query.lower()}%")) | (Book.author.ilike(f"%{query.lower()}%"))
        )

    if rating:
        reviews_query = reviews_query.filter(Review.rating == rating)

    # Определяем порядок сортировки
    order_func = asc if direction == "asc" else desc

    # Сортировка
    if sort == "date":
        reviews_query = reviews_query.order_by(order_func(Review.created_at))
    elif sort == "popularity":
        reviews_query = reviews_query.join(ReviewRating).group_by(Review.id).order_by(
            order_func(func.avg(ReviewRating.rating))
        )
    elif sort == "rating":
        reviews_query = reviews_query.order_by(order_func(Review.rating))

    # Подсчет общего количества отзывов
    total_reviews = reviews_query.count()

    # Применяем пагинацию
    reviews = reviews_query.offset(skip).limit(limit).all()

    if not reviews:
        raise HTTPException(status_code=404, detail="No reviews found")

    # Формируем ответ
    reviews_response = []
    for review in reviews:
        ratings = db.query(ReviewRating).filter(ReviewRating.review_id == review.id).all()
        average_review_rating = sum(rating.rating for rating in ratings) / len(ratings) if ratings else 0

        reviews_response.append({
            "id": review.id,
            "content": review.content,
            "rating": review.rating,
            "book_title": review.book.title,
            "book_author": review.book.author,
            "book_img": review.book.img,
            "username": review.user.username,
            "created_at": review.created_at,
            "genre": review.book.genre,
            "average_review_rating": average_review_rating
        })

    return {"reviews": reviews_response, "total_reviews": total_reviews}


@router.get("/get_rating/{review_id}")
def get_user_rating(
    review_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    existing_rating = db.query(ReviewRating).filter(
        ReviewRating.review_id == review_id,
        ReviewRating.user_id == current_user.id
    ).first()

    return {"user_rating": existing_rating.rating if existing_rating else 0}


@router.post("/rate/{review_id}", response_model=ReviewRatingResponse)
def rate_review(
    review_id: int,
    review_rating: ReviewRatingCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Проверяем, есть ли уже рейтинг от этого пользователя
    existing_rating = db.query(ReviewRating).filter(
        ReviewRating.review_id == review_id, ReviewRating.user_id == current_user.id
    ).first()

    print("existing_rating with review_id=", review_id, existing_rating)

    if existing_rating and review_rating.rating == existing_rating.rating:
        db.delete(existing_rating)
        db.commit()

        ratings = db.query(ReviewRating).filter(ReviewRating.review_id == review_id).all()
        new_avg_rating = sum(r.rating for r in ratings) / len(ratings) if ratings else 0

        review = db.query(Review).filter(Review.id == review_id).first()
        if review:
            review.review_rating = new_avg_rating
            db.commit()
            db.refresh(review)

        return {"user_rating": 0, "average_review_rating": new_avg_rating}

    if existing_rating:
        # Если рейтинг уже был, обновляем его
        existing_rating.rating = review_rating.rating
    else:
        # Если пользователь еще не ставил рейтинг, создаем новый
        new_rating = ReviewRating(
            review_id=review_id,
            user_id=current_user.id,
            rating=review_rating.rating
        )
        db.add(new_rating)

    db.commit()

    # Загружаем отзыв и обновляем его, чтобы увидеть изменения
    review = db.query(Review).filter(Review.id == review_id).first()
    db.refresh(review)

    # Пересчитываем средний рейтинг
    ratings = db.query(ReviewRating).filter(ReviewRating.review_id == review_id).all()
    review.review_rating = sum(r.rating for r in ratings) / len(ratings) if ratings else 0

    db.commit()
    db.refresh(review)

    return {"user_rating": review_rating.rating, "average_review_rating": review.review_rating}


@router.put("/{review_id}", response_model=ReviewResponse)
def update_review(review_id: int, review_update: ReviewUpdate, db: Session = Depends(get_db),
                  current_user: User = Depends(get_current_user)):
    review = db.query(Review).filter(Review.id == review_id,
                                     Review.user_id == current_user.id).first()

    if not review:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Review not found or not owned by you")

    for key, value in review_update.model_dump(exclude_unset=True).items():
        setattr(review, key, value)

    db.commit()
    db.refresh(review)

    return {
        "id": review.id,
        "content": review.content,
        "rating": review.rating,
        "book_title": review.book.title,
        "book_author": review.book.author,
        "book_img": review.book.img,
        "username": current_user.username,
        "created_at": review.created_at,
        "genre": review.book.genre
    }


@router.delete("/{review_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_review(review_id: int, db: Session = Depends(get_db),
                  current_user: User = Depends(get_current_user)):
    review = db.query(Review).filter(Review.id == review_id,
                                     Review.user_id == current_user.id).first()

    if not review:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Review not found or not owned by you")

    db.delete(review)
    db.commit()

    return {"detail": "Review deleted successfully"}
