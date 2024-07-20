from cuid2 import Cuid
from django.db import models as m


def generate_cuid():
    return Cuid(length=32).generate()


class BaseModel(m.Model):
    id = m.CharField(
        max_length=32,
        unique=True,
        primary_key=True,
        db_index=True,
        editable=False,
        default=generate_cuid,
    )
    created = m.DateTimeField(auto_now_add=True)
    modified = m.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
