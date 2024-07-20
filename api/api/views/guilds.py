from rest_framework.viewsets import ModelViewSet

from api.models import Guild
from api.serializers import GuildSerializer


class GuildViewSet(ModelViewSet):
    queryset = Guild.objects.all()
    serializer_class = GuildSerializer
