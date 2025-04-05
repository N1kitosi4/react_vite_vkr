from sqlalchemy.orm import relationship, Mapped, mapped_column
from app.db.database import Base


class Book(Base):
    __tablename__ = 'books'

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    title: Mapped[str] = mapped_column(nullable=False)
    author: Mapped[str] = mapped_column(nullable=False)
    genre: Mapped[str] = mapped_column(nullable=False)
    img: Mapped[str] = mapped_column(nullable=True)

    reviews = relationship("Review", back_populates="book")
