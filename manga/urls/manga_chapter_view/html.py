from django.urls import path

from manga.views.manga_chapter_view import html

urlpatterns = [
    path('manga/<int:manga_id>/chapters/<str:chapter_number>', html.manga_chapter_view),
]