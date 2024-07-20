from django.contrib.auth.models import User
from django.db import models as m
from ordered_model.models import OrderedModel

from api.enums import AvailabilityStatus

from .base import BaseModel


class UserProfile(BaseModel):
    user = m.OneToOneField(User, on_delete=m.CASCADE)
    discriminator = m.PositiveSmallIntegerField()
    avatar = m.ImageField(max_length=255, null=True, blank=True)
    cover = m.ImageField(max_length=255, null=True, blank=True)
    availability_status = m.CharField(
        max_length=16,
        choices=AvailabilityStatus.choices,
        default=AvailabilityStatus.ONLINE,
    )

    def __str__(self):
        return f"{self.user.username}#{self.discriminator:04}"

    class Meta:
        ordering = ["user__username"]
        unique_together = ["user", "discriminator"]


class UserGuildOrder(OrderedModel, BaseModel):
    user = m.OneToOneField(User, on_delete=m.CASCADE)
    guild = m.ForeignKey("Guild", on_delete=m.CASCADE)

    order_with_respect_to = "user"

    class Meta:
        ordering = ["user", "order"]
