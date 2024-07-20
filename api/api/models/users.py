from django.contrib.auth.models import User
from django.db import models as m

from api.enums import AvailabilityStatus

from .base import BaseModel


class UserProfile(BaseModel):
    user = m.OneToOneField(User, on_delete=m.CASCADE)
    avatar = m.ImageField(max_length=255)
    cover = m.ImageField(max_length=255)
    availability_status = m.CharField(
        max_length=16,
        choices=AvailabilityStatus.choices,
        default=AvailabilityStatus.ONLINE,
    )
