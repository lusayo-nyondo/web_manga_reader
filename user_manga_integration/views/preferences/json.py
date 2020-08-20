
from django.http import JsonResponse

from django.contrib.auth.decorators import login_required

from manga.models import Manga

from users import session as user_session
from user_manga_integration.models import UserMangaReadingSettings

@login_required
def set_manga_reading_mode(request):
    user = user_session.get_authenticated_user(request)
    manga_id = request.GET.get('manga')
    reading_mode = request.GET.get('reading_mode')

    response = None
    
    try:
        manga = Manga.objects.get(
            id=manga_id
        )

        manga_reading_settings = UserMangaReadingSettings.objects.get_or_create(
            user=user,
            manga=manga
        )[0]

        manga_reading_settings.reading_mode = reading_mode.upper()

        manga_reading_settings.save()

        response = {
            'status': 'success',
            'description': 'Your reading preferences have been saved accordingly.',
        }

    except Manga.DoesNotExist:
        response = {
            'status': 'failed',
            'description': 'The manga specified in the request does not exist.'
        }
    
    return JsonResponse(response, safe=False)