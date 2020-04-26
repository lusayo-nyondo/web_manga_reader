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

    @property
    def comments(self):
        comments = Post.objects.filter(
            responding_to=self,
        )

        return comments

    @property
    def likes(self):
        likes = Like.objects.filter(
            post=self,
        )

        return likes

class Like(models.Model):
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
    )

    user = models.ForeignKey(
       SiteUser,
       on_delete=models.CASCADE, 
    )

    created_on = models.DateTimeField(
        auto_now_add=True,
    )

    updated_on = models.DateTimeField(
        auto_now=True,
    )

