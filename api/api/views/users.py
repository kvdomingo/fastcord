from rest_framework.viewsets import ModelViewSet

from api.models import UserProfile
from api.serializers import UserProfileSerializer


class UserProfileViewSet(ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
