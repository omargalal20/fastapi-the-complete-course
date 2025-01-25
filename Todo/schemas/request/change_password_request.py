from pydantic import BaseModel, Field


class ChangePasswordRequest(BaseModel):
    old_password: str = Field(...)
    new_password: str = Field(...)

    class Config:
        json_schema_extra = {
            "example": {
                "old_password": "verycomplexpassword",
                "new_password": "morecomplexpassword",
            }
        }
