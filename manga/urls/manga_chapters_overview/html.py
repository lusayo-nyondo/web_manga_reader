from django.urls import path

from manga.views.manga_chapters_overview import html

urlpatterns = [
    path('manga/<int:manga_id>', html.manga_chapters_overview),
]