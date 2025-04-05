from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime
from typing import Optional, Annotated


class ReviewBase(BaseModel):
    content: str
    rating: Annotated[float, Field(gt=0, le=5)]
    review_rating: Optional[float] = 0  # Рейтинг от других пользователей


class ReviewCreate(ReviewBase):
    book_title: str
    book_author: str


class ReviewUpdate(ReviewBase):
    pass


class ReviewResponse(ReviewBase):
    id: int
    username: str
    book_title: str
    book_author: str
    genre: str
    book_img: Optional[str] = None
    created_at: datetime
    average_review_rating: Optional[float] = 0  # Средний рейтинг отзывов

    model_config = ConfigDict(from_attributes=True)


class ReviewRatingCreate(BaseModel):
    rating: float = Field(gt=0, le=5)


class ReviewRatingResponse(BaseModel):
    user_rating: float
    average_review_rating: float


class ReviewsWithPaginationResponse(BaseModel):
    reviews: list[ReviewResponse]
    total_reviews: int

    model_config = ConfigDict(from_attributes=True)
