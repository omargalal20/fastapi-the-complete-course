from data.library import Book
from schemas.books.book_request import BookRequest


def book_mapper(dto: BookRequest) -> Book:
    """
    Maps a BookRequest DTO to a Book entity.

    :param dto: BookRequest object
    :return: Book object
    """
    return Book(
        id=dto.id or 0,  # Use 0 if ID is not provided (e.g., on create)
        title=dto.title,
        author=dto.author,
        description=dto.description,
        rating=dto.rating,
        published_date=dto.published_date
    )
