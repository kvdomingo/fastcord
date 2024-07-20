from django.db import models as m

from api.enums import ChannelType

from .base import BaseModel


class ChannelGroup(BaseModel):
    name = m.CharField(max_length=32, null=False, blank=False, db_index=True)
    order = m.PositiveSmallIntegerField()
    guild = m.ForeignKey("Guild", related_name="channel_groups", on_delete=m.CASCADE)


class Channel(BaseModel):
    name = m.CharField(max_length=32, null=False, blank=False, db_index=True)
    type = m.CharField(
        max_length=8, choices=ChannelType.choices, default=ChannelType.TEXT
    )
    order = m.IntegerField()
    guild = m.ForeignKey("Guild", related_name="channels", on_delete=m.CASCADE)
    group = m.ForeignKey(
        ChannelGroup,
        related_name="channels",
        on_delete=m.SET_NULL,
        default=None,
        null=True,
    )
