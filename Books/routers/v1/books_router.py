from typing import List, Annotated

from fastapi import APIRouter, HTTPException, Path, Query
from starlette import status

from data.library import Book, BOOKS
from mappers import books_mapper
from schemas.params.book_params import GetManyParams
from schemas.request.book_request import ManageOneRequest
from schemas.response.book_response import BookResponse

router = APIRouter(prefix="/books")


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_one(book_request: ManageOneRequest) -> BookResponse:
    created_book: Book = books_mapper.to_book(book_request)

    BOOKS.append(created_book)

    response = books_mapper.to_book_response(created_book)

    return response


@router.get("", status_code=status.HTTP_200_OK)
async def get_many(params: Annotated[GetManyParams, Query()]) -> List[
    BookResponse]:
    filtered_books = BOOKS

    if params.author:
        filtered_books = [book for book in filtered_books if params.author.lower() in book.author.lower()]

    if params.rating:
        filtered_books = [book for book in filtered_books if book.rating.__eq__(params.rating)]

    if params.published_date:
        filtered_books = [book for book in filtered_books if book.published_date.__eq__(params.published_date)]

    response = books_mapper.to_many_book_response(filtered_books)

    return response


@router.get("/{id}", status_code=status.HTTP_200_OK)
async def get_one(id: Annotated[int, Path(title="The ID of the item to get", gt=0)]) -> BookResponse:
    book = next((book for book in BOOKS if book.id.__eq__(id)), None)

    if book is None:
        raise HTTPException(status_code=404, detail=f"Book with id '{id}' not found.")

    response = books_mapper.to_book_response(book)

    return response


@router.put("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_one(id: Annotated[int, Path(title="The ID of the item to get", gt=0)],
                     book_request: ManageOneRequest):
    updated_book: Book = books_mapper.to_updated_book(id, book_request)
    book_changed = False

    for i in range(len(BOOKS)):
        if BOOKS[i].id.__eq__(id):
            BOOKS[i] = updated_book
            book_changed = True

    if not book_changed:
        raise HTTPException(status_code=404, detail=f"Book with id '{id}' not found.")


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_one(id: Annotated[int, Path(title="The ID of the item to get", gt=0)]):
    book_changed = False
    for i in range(len(BOOKS)):
        if BOOKS[i].id == id:
            BOOKS.pop(i)
            book_changed = True
            break
    if not book_changed:
        raise HTTPException(status_code=404, detail=f"Book with id '{id}' not found.")
