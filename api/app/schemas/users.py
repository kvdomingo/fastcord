from pydantic import BaseModel, Field

from app.db.generated.models import AvailabilityStatus
from app.db.generated.users import UpdateUserParams
from app.schemas.validators import UpdateValidatorMixin


class CreateUserSchema(BaseModel):
    username: str
    discriminator: int
    email: str
    avatar: str | None = Field(None)
    cover: str | None = Field(None)
    availability_status: AvailabilityStatus | None = Field(None)


class UpdateUserSchema(UpdateUserParams, UpdateValidatorMixin):
    pass
