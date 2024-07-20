from django.db import models as m

from .base import BaseModel


class Emoji(BaseModel):
    name = m.CharField(max_length=16, null=False, blank=False, db_index=True)
    source = m.ImageField(max_length=255, null=False, blank=False)
    guild = m.ForeignKey("Guild", related_name="emojis", on_delete=m.CASCADE)
    author = m.ForeignKey(
        "UserProfile", related_name="emojis", on_delete=m.SET_NULL, null=True
    )

    def __str__(self):
        return f"{self.guild.name} / {self.name}"

    class Meta:
        ordering = ["guild", "-created"]
