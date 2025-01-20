from pydantic import BaseModel


class BookResponse(BaseModel):
    id: int
    title: str
    author: str
    description: str
    rating: int
    published_date: int

    model_config = {
        "json_schema_extra": {
            "example": {
                "title": "A new book",
                "author": "codingwithroby",
                "description": "A new description of a book",
                "rating": 5,
                'published_date': 2029
            }
        }
    }
