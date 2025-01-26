from pydantic import BaseModel, Field, EmailStr

from ...data.models.user import Role


class ManageOneRequest(BaseModel):
    username: str = Field(...)
    email: EmailStr = Field(...)
    first_name: str = Field(...)
    last_name: str = Field(...)
    password: str = Field(...)
    is_active: bool = Field(...)
    role: Role = Field(...)
    phone_number: str = Field(...)

    class Config:
        json_schema_extra = {
            "example": {
                "username": "johndoe",
                "email": "john.doe@example.com",
                "first_name": "John",
                "last_name": "Doe",
                "phone_number": "111-111-1111",
                "password": "verycomplexpassword",
                "is_active": True,
                "role": "USER"
            }
        }
