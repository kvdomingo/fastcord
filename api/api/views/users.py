from rest_framework.viewsets import ModelViewSet

from api.models import UserGuildOrder, UserProfile
from api.serializers import UserGuildOrderSerializer, UserProfileSerializer


class UserProfileViewSet(ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer


class UserGuildOrderViewSet(ModelViewSet):
    queryset = UserGuildOrder.objects.all()
    serializer_class = UserGuildOrderSerializer
