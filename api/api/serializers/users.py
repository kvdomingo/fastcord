from ordered_model.serializers import OrderedModelSerializer
from rest_framework.serializers import ModelSerializer

from api.models import UserGuildOrder, UserProfile


class UserProfileSerializer(ModelSerializer):
    class Meta:
        model = UserProfile
        fields = "__all__"


class UserGuildOrderSerializer(OrderedModelSerializer):
    class Meta:
        model = UserGuildOrder
        fields = "__all__"
