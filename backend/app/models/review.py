from sqlalchemy import ForeignKey, TIMESTAMP, text, Float
from sqlalchemy.orm import relationship, Mapped, mapped_column
from app.db.database import Base


class Review(Base):
    __tablename__ = 'reviews'

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    content: Mapped[str] = mapped_column(nullable=False)
    rating: Mapped[float] = mapped_column(nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id', ondelete="CASCADE"))
    book_id: Mapped[int] = mapped_column(ForeignKey('books.id', ondelete="CASCADE"))
    created_at = mapped_column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))

    # Поле для рейтинга от других пользователей
    review_rating: Mapped[float] = mapped_column(Float, default=0)

    user = relationship("User", back_populates="reviews")
    book = relationship("Book", back_populates="reviews")
    ratings = relationship("ReviewRating", back_populates="review")


class ReviewRating(Base):
    __tablename__ = 'review_ratings'

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    review_id: Mapped[int] = mapped_column(ForeignKey('reviews.id', ondelete="CASCADE"))
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id', ondelete="CASCADE"))
    rating: Mapped[float] = mapped_column(Float, nullable=False)

    user = relationship("User", back_populates="review_ratings")
    review = relationship("Review", back_populates="ratings")
