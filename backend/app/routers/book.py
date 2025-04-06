import uuid
import shutil
from pathlib import Path

from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy import func
from sqlalchemy.orm import Session
from app.models.book import Book
from app.schemas.book import BookCreate, BookResponse, BookUpdate
from app.db.database import get_db

router = APIRouter()

UPLOAD_DIR = Path("app/uploads/book_images")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=BookResponse)
def create_book(book: BookCreate, db: Session = Depends(get_db)):
    already_exists_book = db.query(Book).filter(func.lower(Book.title) == book.title.lower(),
                                                func.lower(Book.author) == book.author.lower(),
                                                Book.genre == book.genre
                                                ).first()
    if already_exists_book:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=("""Книга уже существует,
                                                                       попробуйте другую книгу.""")
        )
    new_book = Book(**book.model_dump())
    if new_book.title == "" or new_book.author == "" or new_book.genre == "":
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Empty field"
        )
    db.add(new_book)
    db.commit()
    db.refresh(new_book)
    return new_book


@router.get("/{book_id}", response_model=BookResponse)
def get_book(book_id: int, db: Session = Depends(get_db)):
    book = db.query(Book).filter(Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Книга не найдена")
    return book


@router.get("/list_books/{genre}", response_model=list[BookResponse])
def get_books_by_genre(genre: str, db: Session = Depends(get_db)):
    books = (db.query(Book).filter(Book.genre == genre).
             group_by(Book.author, Book.id).all())
    if not books:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail="Книги не найдены")
    return books


@router.get("/", response_model=list[BookResponse])
def list_books(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    books = db.query(Book).offset(skip).limit(limit).all()
    if not books:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail="Книги не найдены")
    return books


@router.put("/{book_id}", response_model=BookResponse)
def update_book(book_id: int, book_update: BookUpdate, db: Session = Depends(get_db)):
    book = db.query(Book).filter(Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Книга не найдена")

    for key, value in book_update.model_dump().items():
        if value == "" and key != "img":
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                                detail="Empty field")
        setattr(book, key, value)
    db.commit()
    db.refresh(book)
    return book


@router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_book(book_id: int, db: Session = Depends(get_db)):
    book = db.query(Book).filter(Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Книга не найдена")
    db.delete(book)
    db.commit()
    return {"detail": "Book deleted successfully"}


@router.post("/upload-book-image/{book_id}", status_code=status.HTTP_200_OK)
def upload_book_image(book_id: int, file: UploadFile = File(...),
                      db: Session = Depends(get_db)):
    book = db.query(Book).filter(Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Книга не найдена")

    file_ext = file.filename.split(".")[-1]
    file_name = f"{uuid.uuid4()}.{file_ext}"
    file_path = UPLOAD_DIR / file_name

    with file_path.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    book.img = f"/static/book_images/{file_name}"
    db.commit()
    db.refresh(book)

    return {"img_url": book.img}
