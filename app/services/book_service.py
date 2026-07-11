from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.book import Book
from app.repositories.book_repository import BookRepository
from app.schemas.book import BookCreate, BookUpdate


class BookService:

    def __init__(self, db: Session):
        self.repository = BookRepository(db)

    def create_book(self, schema: BookCreate) -> Book:
        book = Book(
            title=schema.title,
            author=schema.author,
        )

        return self.repository.create(book)

    def get_books(self) -> list[Book]:
        return self.repository.get_all()

    def get_book(self, book_id: int) -> Book:
        book = self.repository.get_by_id(book_id)

        if book is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Book not found",
            )

        return book

    def update_book(
        self,
        book_id: int,
        schema: BookUpdate,
    ) -> Book:

        book = self.get_book(book_id)

        if schema.title is None and schema.author is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="At least one field must be provided",
            )

        if schema.title is not None:
            book.title = schema.title

        if schema.author is not None:
            book.author = schema.author

        return self.repository.update(book)

    def delete_book(self, book_id: int) -> None:
        book = self.get_book(book_id)

        self.repository.delete(book)