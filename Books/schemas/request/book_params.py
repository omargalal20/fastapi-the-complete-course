from pydantic import BaseModel, Field


class GetManyParams(BaseModel):
    author: str | None = Field(
        default=None, title="The description of the item", max_length=50
    )
    rating: int | None = Field(
        default=None, title="The description of the item", gt=1, lt=6
    )
    published_date: int | None = Field(
        default=None, title="The description of the item", gt=1999, lt=2031
    )
