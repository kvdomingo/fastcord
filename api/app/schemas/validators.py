from fastapi import HTTPException
from pydantic import model_validator
from starlette import status


class UpdateValidatorMixin:
    @model_validator(mode="before")
    def non_empty_body_validation(cls, data):
        if isinstance(data, dict):
            if not any(v for v in data.values() if v != "id"):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="At least one field must be provided.",
                )
        return data
