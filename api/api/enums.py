from django.db.models import TextChoices
from django.utils.translation import gettext_lazy as _


class ChannelType(TextChoices):
    TEXT = "TEXT", _("Text")
    VOICE = "VOICE", _("Voice")


class AvailabilityStatus(TextChoices):
    ONLINE = "ONLINE", _("Online")
    DO_NOT_DISTURB = "DO_NOT_DISTURB", _("Do Not Disturb")
    IDLE = "IDLE", _("Idle")
    OFFLINE = "OFFLINE", _("Offline")
