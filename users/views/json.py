
from django.http import JsonResponse

from django.contrib.auth.decorators import login_required

from users import session as user_session
from users.models import SiteUser


@login_required
def edit(request):
    user_email = request.GET.get('user_email')
    user_firstname = request.GET.get('first_name')
    user_lastname = request.GET.get('last_name')

    receive_notifications = request.GET.get('receive_notifications')
    receive_notifications = True if receive_notifications == 'on' else False
    
    print(receive_notifications)

    response = None

    if user_email and user_firstname and user_lastname:
        user = user_session.get_authenticated_user(request)
        
        user.email = user_email
        user.first_name = user_firstname
        user.last_name = user_lastname
        user.receive_notifications = receive_notifications

        user.save()

        response = {
            'status': 'success',
            'summary': 'The account was edited successfully.',
            'user': {
                'user_email': user_email,
                'first_name': user_firstname,
                'last_name': user_lastname,
                'receive_notifications': receive_notifications,
            }
        }
    else:
        response = {
            'status': 'failed',
            'summary': 'The account was not edited because there is something wrong with the request body.',
        }

    return JsonResponse(response, safe=False)
