from django.core import serializers
from django.http import JsonResponse, HttpResponse

from manga.models import Manga

from users import session as user_session
from users.models import SiteUser

from user_manga_integration.session import validator as user_manga_session_request_validator
from user_manga_integration.session import watchlist as user_watchlist

### START MANGA WATCHLIST HANDLERS

def add_manga_to_user_watchlist(request):
    request_validation = user_manga_session_request_validator.validate_request(request)

    if request_validation['status'] == 'success':
        user = request_validation['user']
        manga = request_validation['manga']

        is_manga_in_user_watchlist = user_watchlist.is_manga_in_user_watchlist(user, manga)

        if is_manga_in_user_watchlist:
            response = {
                'status': 'success',
                'description': 'The manga is already in your watchlist.',
            }
        else:
            success = user_watchlist.add_manga_to_user_watchlist(user, manga)
        
            if success:
                response = {
                    'status': 'success',
                    'description': 'The manga has been added to your watchlist successfully.',
                }
            else:
                response = {
                    'status': 'failed',
                    'description': 'The manga has not been added to your watchlist.',
                }
    else:
        response = request_validation
    
    return JsonResponse(response, safe=False)

def is_manga_in_user_watchlist(request):
    request_validation = user_manga_session_request_validator.validate_request(request)

    if request_validation['status'] == 'success':
        user = request_validation['user']
        manga = request_validation['manga']

        is_manga_in_user_watchlist = user_watchlist.is_manga_in_user_watchlist(user, manga)
    
        if is_manga_in_user_watchlist:
            response = {
                'status': 'success',
                'is_manga_in_user_watchlist': True,
                'description': 'The manga has been found in the user\'s watchlist.',
            }
        else:
            response = {
                'status': 'success',
                'is_manga_in_user_watchlist': False,
                'description': 'The manga has not been found in the user\'s watchlist.',
            }
    else:
        response = request_validation

    return JsonResponse(response, safe=False)

def remove_manga_from_user_watchlist(request):
    request_validation = user_manga_session_request_validator.validate_request(request)
    response = None

    if request_validation['status'] == 'success':
        user = request_validation['user']
        manga = request_validation['manga']

        success = user_watchlist.remove_manga_from_user_watchlist(user, manga)

        if success:
            response = {
                'status': 'success',
                'description': 'The manga has been removed from your watchlist',
            }
        else:
            response = {
                'status': 'failed',
                'description': 'This manga wasn\'t in your watchlist.',
            }
    else:
        response = request_validation

    return JsonResponse(response, safe=False)
 
### END MANGA WATCHLIST HANDLERS
