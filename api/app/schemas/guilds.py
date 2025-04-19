from fastapi import HTTPException
from pydantic import BaseModel, Field, model_validator
from starlette import status


class CreateGuildSchema(BaseModel):
    name: str
    avatar: str | None = Field(None)
    banner: str | None = Field(None)


class UpdateGuildSchema(BaseModel):
    name: str | None = Field(None)
    avatar: str | None = Field(None)
    banner: str | None = Field(None)

    @model_validator(mode="before")
    def non_empty_body_validation(cls, data):
        if isinstance(data, dict):
            if not any(data.values()):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="At least one field must be provided.",
                )
        return data
