from typing import List

from data.library import Book, BOOKS
from schemas.request.book_request import BookRequest
from schemas.response.book_response import BookResponse


def find_book_id(books: List[Book]) -> int:
    return 1 if len(books) == 0 else books[-1].id + 1


def to_book_mapper(dto: BookRequest) -> Book:
    """
    Maps a BookRequest DTO to a Book entity.

    :param dto: BookRequest object
    :return: Book object
    """
    return Book(
        id=find_book_id(BOOKS),
        title=dto.title,
        author=dto.author,
        description=dto.description,
        rating=dto.rating,
        published_date=dto.published_date
    )


def to_book_response_mapper(book: Book) -> BookResponse:
    """
    Maps a BookRequest DTO to a Book entity.

    :param book: Book object
    :return: BookResponse object
    """
    return BookResponse(
        title=book.title,
        author=book.author,
        description=book.description,
        rating=book.rating,
        published_date=book.published_date
    )

def to_books_response_mapper(books: List[Book]) -> List[BookResponse]:
    """
    Maps a list of Book objects to a list of BookResponse DTOs.

    :param books: List of Book objects
    :return: List of BookResponse objects
    """
    return [book_response_mapper(book) for book in books]
