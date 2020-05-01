from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', include('manga.urls')),
    path('oauth/', include('social_django.urls', namespace='social')),
    path('admin/', admin.site.urls),
    path('manga/', include('manga.urls')),
    path('account/', include('users.urls')),
    path('manga_site/', include('user_manga_integration.urls')),
    path('social_integration/', include('social_integration.urls')),
]