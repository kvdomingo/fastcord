from django.db import models as m

from .base import BaseModel


class Guild(BaseModel):
    name = m.CharField(max_length=64, null=False, blank=False, db_index=True)
    avatar = m.ImageField(max_length=255)
    banner = m.ImageField(max_length=255)

    def __str__(self):
        return self.name
