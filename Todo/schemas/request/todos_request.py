from pydantic import BaseModel, Field


class ManageOneRequest(BaseModel):
    title: str = Field(..., min_length=3)
    description: str = Field(..., min_length=3, max_length=100)
    priority: int = Field(..., gt=0, lt=6)
    complete: bool = Field(...)

    class Config:
        json_schema_extra = {
            "example": {
                "title": "Buy groceries",
                "description": "Milk, eggs, and bread",
                "priority": 2,
                "complete": False,
            }
        }

