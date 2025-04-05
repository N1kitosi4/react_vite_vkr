from sqlalchemy import TIMESTAMP, text, Boolean
from sqlalchemy.orm import relationship, Mapped, mapped_column
from app.db.database import Base


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    username: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(unique=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(nullable=False)
    avatar: Mapped[str] = mapped_column(nullable=True)
    created_at = mapped_column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text('now()'))
    is_verified: Mapped[bool] = mapped_column(Boolean, default=False)

    reviews = relationship("Review", back_populates="user")
    # Связь с рейтингами отзывов, которые ставит пользователь
    review_ratings = relationship("ReviewRating", back_populates="user")
