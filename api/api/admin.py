from allauth.account.decorators import secure_admin_login
from django.contrib import admin

admin.autodiscover()
admin.site.login = secure_admin_login(admin.site.login)
