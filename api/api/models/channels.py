from django.db import models as m
from ordered_model.models import OrderedModel

from api.enums import ChannelType

from .base import BaseModel


class ChannelGroup(OrderedModel, BaseModel):
    name = m.CharField(max_length=32, null=False, blank=False, db_index=True)
    guild = m.ForeignKey("Guild", related_name="channel_groups", on_delete=m.CASCADE)

    order_with_respect_to = "guild"

    class Meta:
        ordering = ["guild", "order"]


class Channel(OrderedModel, BaseModel):
    name = m.CharField(max_length=32, null=False, blank=False, db_index=True)
    type = m.CharField(
        max_length=8, choices=ChannelType.choices, default=ChannelType.TEXT
    )
    guild = m.ForeignKey("Guild", related_name="channels", on_delete=m.CASCADE)
    group = m.ForeignKey(
        ChannelGroup,
        related_name="channels",
        on_delete=m.SET_NULL,
        default=None,
        null=True,
    )

    order_with_respect_to = "group"

    class Meta:
        ordering = ["guild", "group", "order"]
