from django.db import models

from users.models import SiteUser
class Post(models.Model):
    user = models.ForeignKey(
        SiteUser,
        on_delete=models.CASCADE
    )

    url = models.URLField()

    responding_to = models.ForeignKey(
        'self',
        blank=True,
        null=True,
        on_delete=models.CASCADE
    )

    text = models.TextField()

    created_on = models.DateTimeField(
        auto_now_add=True,
    )

    updated_on = models.DateTimeField(
        auto_now=True,
    )
