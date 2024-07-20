from rest_framework.serializers import ModelSerializer

from api.models import Emoji


class EmojiSerializer(ModelSerializer):
    class Meta:
        model = Emoji
        fields = "__all__"
