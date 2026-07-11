from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.book import BookCreate, BookResponse, BookUpdate
from app.services.book_service import BookService

router = APIRouter(
    prefix="/books",
    tags=["books"],
)


def get_book_service(
    db: Session = Depends(get_db),
) -> BookService:
    return BookService(db)


@router.post(
    "/",
    response_model=BookResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_book(
    schema: BookCreate,
    service: BookService = Depends(get_book_service),
):
    return service.create_book(schema)


@router.get(
    "/",
    response_model=list[BookResponse],
)
def get_books(
    service: BookService = Depends(get_book_service),
):
    return service.get_books()


@router.get(
    "/{book_id}",
    response_model=BookResponse,
)
def get_book(
    book_id: int,
    service: BookService = Depends(get_book_service),
):
    return service.get_book(book_id)


@router.patch(
    "/{book_id}",
    response_model=BookResponse,
)
def update_book(
    book_id: int,
    schema: BookUpdate,
    service: BookService = Depends(get_book_service),
):
    return service.update_book(book_id, schema)


@router.delete(
    "/{book_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_book(
    book_id: int,
    service: BookService = Depends(get_book_service),
) -> None:
    service.delete_book(book_id)