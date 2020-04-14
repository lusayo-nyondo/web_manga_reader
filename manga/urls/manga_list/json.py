from django.urls import path

from manga.views.manga_list import json

urlpatterns = [
    path('manga_list_json', json.manga_list_json),
    path('tag_list_json', json.tag_list_json),
    path('author_list_json', json.author_list_json),
    path('manga_page_json/<int:page_number>', json.manga_page_json),
    path('author_page_json/<int:page_number>', json.author_page_json),
    path('tag_page_json/<int:page_number>', json.tag_page_json),
]
