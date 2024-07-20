from rest_framework.serializers import ModelSerializer

from api.models import Guild


class GuildSerializer(ModelSerializer):
    class Meta:
        model = Guild
        fields = "__all__"
