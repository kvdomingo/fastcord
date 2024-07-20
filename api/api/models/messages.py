from django.db import models as m

from .base import BaseModel


class Message(BaseModel):
    content = m.TextField(max_length=2048, null=False, blank=False)
    author = m.ForeignKey(
        "UserProfile", related_name="messages", on_delete=m.SET_NULL, null=True
    )
    channel = m.ForeignKey("Channel", related_name="messages", on_delete=m.CASCADE)
