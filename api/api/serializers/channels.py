from rest_framework.serializers import ModelSerializer

from api.models import Channel, ChannelGroup


class ChannelGroupSerializer(ModelSerializer):
    class Meta:
        model = ChannelGroup
        fields = "__all__"


class ChannelSerializer(ModelSerializer):
    class Meta:
        model = Channel
        fields = "__all__"
