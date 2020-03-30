from manga.models import Manga

from users import session as user_session
from users.models import SiteUser

def validate_request(request):
    manga_id = None
    user_id = None

    try:
        manga_id = request.GET.get("manga_id")
        user_id = request.GET.get("user_id")

        active_user = user_session.get_authenticated_user(request)

        response = None

        if user_id == None:
            response = {
                'status': 'failed',
                'description': 'No user was specified for this request. If you\'re already logged in, log in again then retry.',
            }
        elif active_user == None:
            response = {
                'status': 'failed',
                'description': 'You are not logged in. Please sign up or login to your account.',
            }
        elif int(user_id) == active_user.id:
            manga = Manga.objects.get(
                id=manga_id
            )

            user = SiteUser.objects.get(
                id=user_id
            )

            response = {
                'status': 'success',
                'manga': manga,
                'user': user,
            }
        else:
            response = {
                'status': 'failed',
                'description': 'The user specified in the request is not the currently active user.'
            }
    except KeyError:
        response = {
            'status': 'failed',
            'description': 'Malformed request. Either user or manga has not been specified.',
        }
    
    return response