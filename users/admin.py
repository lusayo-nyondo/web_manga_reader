from django.contrib import admin
from .models import SiteUser, ExternalAccount
# Register your models here.

admin.site.register(SiteUser)
admin.site.register(ExternalAccount)
