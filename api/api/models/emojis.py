from django.db import models as m

from .base import BaseModel


class Emoji(BaseModel):
    name = m.CharField(max_length=16, null=False, blank=False)
    source = m.ImageField(max_length=255, null=False, blank=False)
    guild = m.ForeignKey("Guild", related_name="emojis", on_delete=m.CASCADE)
    author = m.ForeignKey(
        "UserProfile", related_name="emojis", on_delete=m.SET_NULL, null=True
    )

    class Meta:
        ordering = ["guild", "-created"]
