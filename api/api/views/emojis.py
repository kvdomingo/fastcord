from rest_framework.viewsets import ModelViewSet

from api.models import Emoji
from api.serializers import EmojiSerializer


class EmojiViewSet(ModelViewSet):
    queryset = Emoji.objects.all()
    serializer_class = EmojiSerializer
