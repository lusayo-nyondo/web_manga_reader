from django.db import models
from django.utils import timezone

from datetime import timedelta

# Create your models here.


class Author(models.Model):
    STATUS_STRINGS = [
        ('Active', 'Active'),
        ('Unknown', 'Unknown'),
        ('On Hiatus', 'On Hiatus'),
        ('Retired', 'Retired'),
        ('Deceased', 'Deceased'),
    ]

    author_name = models.TextField()
    author_status = models.TextField(choices=STATUS_STRINGS)
    author_url = models.URLField(blank=True)

    def __str__(self):
        return self.author_name


class Translator(models.Model):
    status_strings = [
        ('Active', 'Active'),
        ('Unknown', 'Unknown'),
        ('On Hiatus', 'On Hiatus'),
        ('Disbanded', 'Disbanded')
    ]

    translator_name = models.TextField()
    translator_status = models.TextField(choices=status_strings)
    translator_url = models.URLField(blank=True)

    def __str__(self):
        return self.translator_name


class TagType(models.Model):
    type_name = models.CharField(max_length=200)

    def __str__(self):
        return self.type_name


class Tag(models.Model):
    tag_type = models.ForeignKey(
        TagType,
        default='',
        blank=True,
        null=True,
        on_delete=models.SET_DEFAULT
    )
    
    tag_name = models.CharField(max_length=200)
    
    def __str__(self):
        return self.tag_name


class ExternalResource(models.Model):
    RESOURCE_TYPES = [
        ('Scrapable Web Page', 'Scrapable Web Page'),
        ('Static Resource', 'Static Resource'),
    ]

    RESOURCE_STATUSES = [
        ('Untested', 'Untested'),
        ('Verified', 'Verified'),
        ('Broken', 'Broken'),
    ]

    resource_type = models.CharField(
        max_length=100,
        default='Static Resource Locator',
        choices=RESOURCE_TYPES,
    )

    resource_status = models.CharField(
        max_length=100,
        default='Untested',
        choices=RESOURCE_STATUSES,
    )

    resource_short_name = models.TextField(blank=True)
    url_expression = models.URLField()
    resource_processing_script = models.TextField(blank='True')

    def __str__(self):
        return self.url_expression
    

class AlternateName(models.Model):
    language = models.CharField(max_length=100, blank=True)
    characters = models.CharField(max_length=100, blank=True)
    alternate_name = models.TextField()

    def __str__(self):
        return self.alternate_name


class Manga(models.Model):
    STATUSES = [
        ('Ongoing', 'Ongoing'),
        ('Completed', 'Completed')
    ]

    manga_name = models.TextField()
    
    alternate_names = models.ManyToManyField(
        AlternateName,
        blank=True
    )
    
    manga_year = models.IntegerField(
        blank=True,
        null=True,
        default=0
    )

    manga_status = models.CharField(
        default='Ongoing',
        max_length=100,
        choices=STATUSES
    )
    
    original_publisher = models.CharField(
        max_length=300,
        blank=True,
        default=''
    )
    
    banner_image_url = models.URLField(
        blank=True
    )
    
    chapter_sources = models.ManyToManyField(
        ExternalResource,
        default='',
        blank=True
    )

    views = models.IntegerField(
        default=0
    )
    
    description = models.TextField(
        default="Doesn't have one yet. Feel free to add it."
    )
    
    manga_author = models.ManyToManyField(
        Author,
        default='',
        blank=True
    )
    
    manga_translator = models.ManyToManyField(
        Translator,
        default='',
        blank=True
    )
    
    tags = models.ManyToManyField(
        Tag,
        blank=True
    )
    
    added_on = models.DateTimeField(
        auto_now_add=True
    )
    
    updated_on = models.DateTimeField(
        auto_now=True
    )

    @property
    def valid_ratings(self):
        return range(1, 6)

    @property
    def rating(self):
        from user_manga_integration.models import UserMangaRating

        ratings = UserMangaRating.objects.filter(
            manga=self,
        )

        if len(ratings) == 0:
            return -1
        else:
            ratings_values = ratings.values('rating')

            total_rating_score = 0

            for rating in ratings_values:
                total_rating_score += rating['rating']

            num_ratings = len(ratings)

            value = int(total_rating_score / num_ratings)
            return value
        
    @property
    def chapters(self):
        chapters = Chapter.objects.filter(manga_id=self.id)
        return chapters

    @property   
    def latest_chapter(self):
        chapters = self.chapters    
        chapters.order_by('-added_on')

        if len(chapters) == 0:
            return None
        
        latest_chapter = chapters[0]

        return latest_chapter
            
    def rating_by(self, user):
        from user_manga_integration.models import UserMangaRating

        try:
            rating = UserMangaRating.objects.get(
                manga=self,
                user=user,
            )

            return rating.rating
        except UserMangaRating.DoesNotExist:
            return self.rating
    
    def bookmarked_by(self, user):
        from user_manga_integration.models import UserChapterBookmarkEntry

        chapters = self.chapters

        for chapter in chapters:
            try:
                bookmark_entry = UserChapterBookmarkEntry.objects.filter(
                    chapter=chapter,
                    user=user,
                    is_manually_assigned=True,
                )

                if len(bookmark_entry) > 0:
                    return chapter
            except UserChapterBookmarkEntry.DoesNotExist:
                continue

        return None

    def last_read_by(self, user):
        from user_manga_integration.models import UserChapterHistoryEntry

        chapters = self.chapters

        last_read = None
        last_read_datetime = timezone.now() - timedelta(days=36524)

        for chapter in chapters:
            try:
                history_entries = UserChapterHistoryEntry.objects.filter(
                    chapter=chapter,
                    user=user,
                )

                for history_entry in history_entries:
                    if history_entry.updated_on > last_read_datetime:
                        last_read_datetime = history_entry.updated_on
                        last_read = chapter
                        
            except UserChapterHistoryEntry.DoesNotExist:
                continue

        return last_read
    
    def __str__(self):
        return self.manga_name

class Volume(models.Model):
    owning_manga = models.ForeignKey(
        Manga,
        blank=True,
        null=True,
        on_delete=models.SET_NULL
    )
    
    volume_number = models.IntegerField(
        default=-1
    )
    
    volume_name = models.TextField(
        default=-1
    )
    
    volume_alternate_names = models.ManyToManyField(
        AlternateName,
        blank=True
    )


class Chapter(models.Model):
    manga = models.ForeignKey(
        Manga,
        default='',
        blank=True,
        null=True,
        on_delete=models.SET_DEFAULT
    )
    volume = models.ForeignKey(Volume,
        default='',
        blank=True,
        null=True,
        on_delete=models.SET_DEFAULT
    )

    chapter_number = models.CharField(default='0', max_length=10)
    chapter_name = models.TextField(blank=True)
    views = models.IntegerField(default=0)
    url = models.URLField(default='https://mangahive.com/manga/notices/resource_pending_authorization')
    external_sources = models.ManyToManyField(ExternalResource, blank=True)
    added_on = models.DateTimeField(auto_now_add=True)
    
    @property
    def views(self):
        from user_manga_integration.models import UserChapterHistoryEntry

        entries = UserChapterHistoryEntry.objects.filter(
            chapter=self,
        )

        return len(entries)

    def __str__(self):
        return self.manga.manga_name + ' - ' + str(self.chapter_number)

    def to_dict(self):
        return {
            'id': self.id,
            'manga_id': self.manga.id,
            'chapter_number': self.chapter_number,
            'views': self.views,
            'url': self.url,
            'adden_on': self.added_on,
        }


class Page(models.Model):
    page_number = models.IntegerField(default=0)
    chapter = models.ForeignKey(Chapter, default='', blank=True, null=True, on_delete=models.SET_DEFAULT)
    source_image_url = models.URLField(default='https://mangahive.com/manga/static/assets/stubs/not_found.jpg')
    external_sources = models.ManyToManyField(ExternalResource, blank=True)

    def __str__(self):
        return self.chapter.__str__() + ' - ' + str(self.page_number)
