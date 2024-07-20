from allauth.account.decorators import secure_admin_login
from django.contrib import admin

from api.models import Channel, ChannelGroup, Emoji, Guild, Message, UserProfile

admin.autodiscover()
admin.site.login = secure_admin_login(admin.site.login)

admin.site.register(Channel)
admin.site.register(ChannelGroup)
admin.site.register(Emoji)
admin.site.register(Guild)
admin.site.register(Message)
admin.site.register(UserProfile)
