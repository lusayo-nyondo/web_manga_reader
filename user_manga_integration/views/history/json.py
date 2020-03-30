from django.http import JsonResponse

from manga.models import Manga

from users import session as user_session

def last_read_json(request):
    response = None

    try:
        manga_id = request.GET.get('manga_id')

        manga = Manga.objects.get(
            id=manga_id
        )

        user = user_session.get_authenticated_user(request)

        chapter = manga.last_read_by(user)

        if chapter:
            chapter = chapter.to_dict()

            response = {
                'status': 'success',
                'chapter': chapter,
            }

        else:
            response = {
                'status': 'last_read_not_found',
            }

    except KeyError:
        response = {
            'status': 'failed',
            'description': 'Manga not found',
        }
    except AttributeError:
        response = {
            'status': 'failed',
            'description': 'User unauthenticated.',
        }

    return JsonResponse(response, safe=False)
