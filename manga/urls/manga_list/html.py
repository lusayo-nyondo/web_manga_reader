from django.urls import path

from manga.views.manga_list import html

urlpatterns = [
    path('', html.index),
    path('manga_list', html.manga_list_all_view),
    path('manga_list_filtered/<int:page_number>', html.manga_list_filtered_view)
]