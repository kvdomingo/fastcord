from pydantic import BaseModel, Field

from app.schemas.validators import UpdateValidatorMixin


class CreateGuildSchema(BaseModel):
    name: str
    avatar: str | None = Field(None)
    banner: str | None = Field(None)


class UpdateGuildSchema(BaseModel, UpdateValidatorMixin):
    name: str | None = Field(None)
    avatar: str | None = Field(None)
    banner: str | None = Field(None)
