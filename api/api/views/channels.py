from rest_framework.viewsets import ModelViewSet

from api.models import Channel, ChannelGroup
from api.serializers import ChannelGroupSerializer, ChannelSerializer


class ChannelViewSet(ModelViewSet):
    queryset = Channel.objects.all()
    serializer_class = ChannelSerializer


class ChannelGroupViewSet(ModelViewSet):
    queryset = ChannelGroup.objects.all()
    serializer_class = ChannelGroupSerializer
