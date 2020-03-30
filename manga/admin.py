from django.contrib import admin
from .models import Manga, Author, TagType, Tag,\
    Translator, Chapter, AlternateName,\
    ExternalResource, Page

# Register your models here.

admin.site.register(Manga)
admin.site.register(Author)
admin.site.register(TagType)
admin.site.register(Tag)
admin.site.register(Translator)
admin.site.register(Chapter)
admin.site.register(AlternateName)
admin.site.register(ExternalResource)
admin.site.register(Page)
