from django.urls import path

from . import views

urlpatterns = [
    path('post_comment', views.post_comment),
    path('fetch_comments', views.fetch_comments),
    path('submit_like', views.submit_like),
    path('submit_reply', views.submit_reply),
]