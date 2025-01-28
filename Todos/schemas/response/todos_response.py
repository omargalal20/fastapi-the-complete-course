from pydantic import BaseModel, Field


class TodosResponse(BaseModel):
    id: int = Field(...)
    title: str = Field(...)
    description: str = Field(...)
    priority: int = Field(...)
    complete: bool = Field(...)

    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "title": "Complete FastAPI Course",
                "description": "Finish the FastAPI course by the end of the week",
                "priority": 1,
                "complete": False
            }
        }
