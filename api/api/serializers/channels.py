from ordered_model.serializers import OrderedModelSerializer

from api.models import Channel, ChannelGroup


class ChannelGroupSerializer(OrderedModelSerializer):
    class Meta:
        model = ChannelGroup
        fields = "__all__"


class ChannelSerializer(OrderedModelSerializer):
    class Meta:
        model = Channel
        fields = "__all__"
