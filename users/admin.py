from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from .forms import SiteUserCreationForm, SiteUserChangeForm
from .models import SiteUser, ExternalAccount

class SiteUserAdmin(UserAdmin):
    add_form = SiteUserCreationForm
    form = SiteUserChangeForm
    model = SiteUser
    list_display = ['email', 'username',]



#admin.site.register(SiteUser)
admin.site.register(ExternalAccount)
admin.site.register(SiteUser, SiteUserAdmin)
