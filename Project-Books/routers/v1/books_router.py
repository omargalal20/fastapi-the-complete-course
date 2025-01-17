from typing import Optional

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter(prefix="/books")

BOOKS = [
    {'title': 'Title One', 'author': 'Author One', 'category': 'science'},
    {'title': 'Title Two', 'author': 'Author Two', 'category': 'science'},
    {'title': 'Title Three', 'author': 'Author Three', 'category': 'history'},
    {'title': 'Title Four', 'author': 'Author Four', 'category': 'math'},
    {'title': 'Title Five', 'author': 'Author Five', 'category': 'math'},
    {'title': 'Title Six', 'author': 'Author Two', 'category': 'math'}
]


class Book(BaseModel):
    title: str
    author: str
    category: str


@router.post("")
async def create_one(book_request: Book):
    created_book = {'title': book_request.title, 'author': book_request.author, 'category': book_request.category}

    BOOKS.append(created_book)

    return created_book


@router.get("")
async def get_many(author: Optional[str] = None, category: Optional[str] = None):
    filtered_books = BOOKS

    if author:
        filtered_books = [book for book in filtered_books if author.lower() in book['author'].lower()]

    if category:
        filtered_books = [book for book in filtered_books if category.lower() in book['category'].lower()]

    return filtered_books


@router.get("/{title}")
async def get_one(title: str):
    book = next((book for book in BOOKS if book['title'].lower() == title.lower()), None)

    if book is None:
        raise HTTPException(status_code=404, detail=f"Book with title '{title}' not found.")

    return book


@router.put("/{title}")
async def update_one(title: str, book_request: Book):
    updated_book = {'title': book_request.title, 'author': book_request.author, 'category': book_request.category}

    for i in range(len(BOOKS)):
        if BOOKS[i].get('title').casefold() == title.casefold():
            BOOKS[i] = updated_book
            return updated_book

    raise HTTPException(status_code=404, detail="Book not found")


@router.delete("/{title}")
async def delete_one(title: str):
    for i in range(len(BOOKS)):
        if BOOKS[i].get('title').casefold() == title.casefold():
            BOOKS.pop(i)
            break
