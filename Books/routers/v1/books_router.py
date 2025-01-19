from typing import Optional

from fastapi import APIRouter, HTTPException
from starlette import status

from data.library import Book, BOOKS
from schemas.books.book_request import BookRequest

router = APIRouter(prefix="/books")


def find_book_id() -> int:
    book_id = 1 if len(BOOKS) == 0 else BOOKS[-1].id + 1
    return book_id


def create_one_mapper(dto: BookRequest) -> Book:
    """
    Maps a BookRequest DTO to a Book entity.

    :param dto: BookRequest object
    :return: Book object
    """
    return Book(
        id=find_book_id(),  # Use 0 if ID is not provided (e.g., on create)
        title=dto.title,
        author=dto.author,
        description=dto.description,
        rating=dto.rating,
        published_date=dto.published_date
    )


@router.post("")
async def create_one(book_request: BookRequest, status_code=status.HTTP_201_CREATED):
    created_book: Book = create_one_mapper(book_request)

    BOOKS.append(created_book)

    return created_book


@router.get("")
async def get_many(author: Optional[str] = None, rating: Optional[int] = None, status_code=status.HTTP_200_OK):
    filtered_books = BOOKS

    if author:
        filtered_books = [book for book in filtered_books if author.lower() in book.author.lower()]

    if rating:
        filtered_books = [book for book in filtered_books if book.rating.__eq__(rating)]

    return filtered_books


@router.get("/{id}")
async def get_one(id: int, status_code=status.HTTP_200_OK):
    book = next((book for book in BOOKS if book.id.__eq__(id)), None)

    if book is None:
        raise HTTPException(status_code=404, detail=f"Book with id '{id}' not found.")

    return book


@router.put("/{id}")
async def update_one(id: int, book_request: BookRequest, status_code=status.HTTP_200_OK):
    updated_book: Book = Book(**book_request.model_dump())

    for i in range(len(BOOKS)):
        if BOOKS[i].id.__eq__(id):
            BOOKS[i] = updated_book
            return updated_book

    raise HTTPException(status_code=404, detail=f"Book with id '{id}' not found.")


@router.delete("/{id}")
async def delete_one(id: int, status_code=status.HTTP_200_OK):
    for i in range(len(BOOKS)):
        if BOOKS[i].id.__eq__(id):
            deleted_book = BOOKS[i]
            BOOKS.pop(i)
            return deleted_book

    raise HTTPException(status_code=404, detail=f"Book with id '{id}' not found.")
