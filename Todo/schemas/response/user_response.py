from pydantic import BaseModel, Field, EmailStr

from data.models.user import Role


class UserResponse(BaseModel):
    id: int = Field(...)
    username: str = Field(...)
    email: EmailStr = Field(...)
    first_name: str = Field(...)
    last_name: str = Field(...)
    is_active: bool = Field(...)
    role: Role = Field(...)

    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "username": "johndoe",
                "email": "john.doe@example.com",
                "first_name": "John",
                "last_name": "Doe",
                "is_active": True,
                "role": "USER"
            }
        }
