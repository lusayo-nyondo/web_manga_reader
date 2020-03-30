from django.http import JsonResponse

from manga.models import Manga

from users import session as user_session

from user_manga_integration.session import ratings

def submit_rating(request):
    response = None

    try:
        manga_id = request.GET.get('manga_id')
        rating = request.GET.get('rating')

        manga = Manga.objects.get(
            id=manga_id
        )


        user = user_session.get_authenticated_user(request)
        
        if user:
            ratings.submit_rating(
                user=user,
                manga=manga,
                rating=int(rating),
            )

            valid_ratings = list(manga.valid_ratings)

            response = {
                'status': 'success',
                'rating': rating,
                'valid_ratings': valid_ratings,
            }
        else:
            response = {
                'status': 'failed',
                'description': 'You have to login to get this functionality.',
            }

    except KeyError:
        response = {
            'status': 'failed',
            'description': 'Manga not found',
        }
    except AttributeError:
        response = {
            'status': 'failed',
            'description': 'User unauthenticated.'
        }
        raise

    return JsonResponse(response, safe=False)
