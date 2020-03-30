# users/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models


class SiteUser(AbstractUser):
    image_url = models.URLField(
        default="/static/accounts/default.png"
    )
    
    receive_notifications = models.BooleanField(
        default=True,
    )

class ExternalAccount(models.Model):
    user = models.ForeignKey(
        SiteUser,
        on_delete=models.CASCADE
    )

    account_name = models.TextField()
    full_name = models.TextField(default='', blank=True, null=True)
    image_url = models.URLField()
    auth_token = models.TextField()

    def __str__(self):
        return self.account_name
