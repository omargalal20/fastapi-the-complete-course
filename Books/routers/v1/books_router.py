from typing import Optional, List

from fastapi import APIRouter, HTTPException

from data.library import Book, BOOKS
from mappers.books import to_book_response_mapper, to_book_mapper, to_books_response_mapper
from schemas.request.book_request import BookRequest
from schemas.response.book_response import BookResponse

router = APIRouter(prefix="/books")


@router.post("")
async def create_one(book_request: BookRequest) -> BookResponse:
    created_book: Book = to_book_mapper(book_request)

    BOOKS.append(created_book)

    response = to_book_response_mapper(created_book)

    return response


@router.get("")
async def get_many(author: Optional[str] = None, rating: Optional[int] = None) -> List[BookResponse]:
    filtered_books = BOOKS

    if author:
        filtered_books = [book for book in filtered_books if author.lower() in book.author.lower()]

    if rating:
        filtered_books = [book for book in filtered_books if book.rating.__eq__(rating)]

    response = to_books_response_mapper(filtered_books)

    return response


@router.get("/{id}")
async def get_one(id: int) -> BookResponse:
    book = next((book for book in BOOKS if book.id.__eq__(id)), None)

    if book is None:
        raise HTTPException(status_code=404, detail=f"Book with id '{id}' not found.")

    response = to_book_response_mapper(book)

    return response


@router.put("/{id}")
async def update_one(id: int, book_request: BookRequest) -> BookResponse:
    updated_book: Book = Book(**book_request.model_dump())

    for i in range(len(BOOKS)):
        if BOOKS[i].id.__eq__(id):
            BOOKS[i] = updated_book
            response = to_book_response_mapper(BOOKS[i])
            return response

    raise HTTPException(status_code=404, detail=f"Book with id '{id}' not found.")


@router.delete("/{id}")
async def delete_one(id: int) -> BookResponse:
    for i in range(len(BOOKS)):
        if BOOKS[i].id.__eq__(id):
            deleted_book = BOOKS[i]
            BOOKS.pop(i)
            response = to_book_response_mapper(deleted_book)
            return response

    raise HTTPException(status_code=404, detail=f"Book with id '{id}' not found.")
