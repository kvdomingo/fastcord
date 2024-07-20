from django.http.response import HttpResponse
from django.urls import path
from rest_framework.routers import DefaultRouter

from api.views import (
    ChannelGroupViewSet,
    ChannelViewSet,
    EmojiViewSet,
    GuildViewSet,
    MessageViewSet,
    UserGuildOrderViewSet,
    UserProfileViewSet,
)

router = DefaultRouter()
router.register("channels", ChannelViewSet)
router.register("channel-groups", ChannelGroupViewSet)
router.register("emojis", EmojiViewSet)
router.register("guilds", GuildViewSet)
router.register("messages", MessageViewSet)
router.register("profiles", UserProfileViewSet)
router.register("user-guilds", UserGuildOrderViewSet)

urlpatterns = [
    path("health", lambda r: HttpResponse(b"ok")),
    *router.urls,
]
