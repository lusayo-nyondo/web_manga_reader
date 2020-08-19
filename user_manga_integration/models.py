from datetime import datetime

from django.db import models
from users.models import SiteUser
from manga.models import Manga, Chapter, Tag
# Create your models here.

class UserMangaWatchlistEntry(models.Model):
    user = models.ForeignKey(
        SiteUser,
        on_delete=models.CASCADE
    )
    
    manga = models.ForeignKey(
        Manga,
        on_delete=models.CASCADE
    )

    added_on = models.DateTimeField(
        auto_now_add=True,   
    )

    updated_on = models.DateTimeField(
        auto_now=True,
    )
    
    def __str__(self):
        entry_str = '{}-{}'.format(
            self.user.user_name,
            self.manga.manga_name,
        )

        return entry_str


class UserChapterBookmarkEntry(models.Model):
    user = models.ForeignKey(
        SiteUser,
        on_delete=models.CASCADE
    )

    manga = models.ForeignKey(
        Manga,
        on_delete=models.CASCADE
    )

    chapter = models.ForeignKey(
        Chapter,
        on_delete=models.CASCADE
    )

    is_manually_assigned = models.BooleanField(
        default=False,
    )

    added_on = models.DateTimeField(
        auto_now_add=True,
    )

    updated_on = models.DateTimeField(
        auto_now=True,
    )

    def __str__(self):
        entry_str = '{}-{}-{}'.format(
            self.user.username,
            self.manga.manga_name,
            self.chapter.chapter_number,
        )

        return entry_str

class UserChapterHistoryEntry(models.Model):
    user = models.ForeignKey(
        SiteUser,
        on_delete=models.CASCADE
    )

    manga = models.ForeignKey(
        Manga,
        on_delete=models.CASCADE
    )

    chapter = models.ForeignKey(
        Chapter,
        on_delete=models.CASCADE
    )

    #Placeholder for some json serialization magic. This is horrible code.
    chapter_obj = None

    added_on = models.DateTimeField(
        auto_now_add=True,
    )

    updated_on = models.DateTimeField(
        auto_now=True,
    )

    def __str__(self):
        entry_str = '{0}-{1}-{2}'.format(
            self.user.username,
            self.manga.manga_name,
            self.chapter.chapter_number,
        )

        return entry_str
    
class UserTagsSubscriptionEntry(models.Model):
    subscription_name = models.CharField(
        max_length=300,
        default="Anonymous Subscription"
    )

    user = models.ForeignKey(
        SiteUser,
        on_delete=models.CASCADE
    )
    
    added_on = models.DateTimeField(
        auto_now_add=True,
    )

    updated_on = models.DateTimeField(
        auto_now=True,
    )


class UserTagsSubscriptionEntryTag(models.Model):
    tag = models.ForeignKey(
        Tag,
        on_delete=models.CASCADE,
    )

    user_tags_subscription_entry = models.ForeignKey(
        UserTagsSubscriptionEntry,
        on_delete=models.CASCADE,
    )

    added_on = models.DateTimeField(
        auto_now_add=True,
    )

    updated_on = models.DateTimeField(
        auto_now=True,
    )


class UserActivity(models.Model):
    action_time = models.DateTimeField(
        auto_now_add=True
    )

    time_spent_millis = models.FloatField(
        null=True,
        blank=True,
        default=0.0
    )

    page_of_interest = models.URLField(
        blank=True,
        null=True,
        default=''
    )
    
    user = models.ForeignKey(
        SiteUser,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.user.username + " - " + self.page_of_interest


class UserMangaRating(models.Model):
    domain = [ (x, x) for x in range(6) ]

    user = models.ForeignKey(
        SiteUser,
        on_delete=models.CASCADE
    )

    manga = models.ForeignKey(
        Manga,
        on_delete=models.CASCADE,
    )
    
    rating = models.IntegerField(
        choices=domain,
        default=0,
    )

    added_on = models.DateTimeField(
        auto_now_add=True,
    )

    updated_on = models.DateTimeField(
        auto_now=True,
    )

    def __str__(self):
        return str(self.rating_value)


class UserNotificationEvent(models.Model):
    EVENT_TYPES = [
        ('New Chapter Release', 'New Chapter Release'),
        ('Blog Article Release', 'Blog Article Release'),
        ('New Manga Release', 'New Manga Release'),
        ('Merchandise Release', 'Merchandise Release'),
        ('Site Event', 'Site Event'),
    ]

    event_name = models.TextField()
    event_type = models.CharField(
        max_length=100,
        default='New Chapter Release',
        choices=EVENT_TYPES,
    )

    event_description = models.TextField()
    event_banner_image_url = models.URLField(blank=True, null=True)
    event_url = models.URLField()

    affected_manga = models.ManyToManyField(
        Manga,
        blank=True,
    )

    affected_tags = models.ManyToManyField(
        Tag,
        blank=True,
    )

    affected_users = models.ManyToManyField(
        SiteUser,
        blank=True,
    )

    added_on = models.DateTimeField(
        auto_now_add=True,
    )

    updated_on = models.DateTimeField(
        auto_now=True,
    )


READING_MODES = [
    ['SINGLE_PAGE', 'SINGLE_PAGE'],
    ['WEBTOON', 'WEBTOON']
]

READING_THEMES = [
    ['DEFAULT', 'DEFAULT']
]

class UserMangaReadingSettings(models.Model):
    user = models.ForeignKey(
        SiteUser,
        on_delete=models.CASCADE
    )

    manga = models.ForeignKey(
        Manga,
        on_delete=models.CASCADE
    )

    reading_mode = models.CharField(
        max_length = 12,
        choices=READING_MODES
    )

    theme = models.CharField(
        max_length=12,
        choices=READING_THEMES,
        default='DEFAULT'
    )

    def __str__(self):
        return '{user} prefers to read in {reading_mode}'.format(
            user=self.user.__str__(),
            reading_mode=reading_mode
        )
