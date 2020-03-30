
from django.shortcuts import loader
from django.http import JsonResponse

from manga import session as manga_session
from manga.models import Manga, Chapter

from users import session as user_session
from users.models import SiteUser

from user_manga_integration.session import validator as user_manga_session_request_validator
from user_manga_integration.session import bookmarks as user_bookmarks

from user_manga_integration.models import UserChapterBookmarkEntry

def add_chapter_to_user_bookmarks(request):
    request_validation = user_manga_session_request_validator.validate_request(request)
    
    response = None
        
    if request_validation["status"] == "success":
        user = request_validation["user"]
        manga = request_validation["manga"]

        chapter_id = request.GET.get("chapter_id")
        chapter = Chapter.objects.get(
            id=chapter_id,
        )

        is_manga_chapter_in_user_bookmarks = user_bookmarks.is_manga_chapter_in_user_bookmarks(
            user,
            manga,
            chapter,
        )

        if is_manga_chapter_in_user_bookmarks:
            response = {
                'status': 'failed',
                'description': 'This chapter is already in your bookmarks.',
            }

        else:
            user_bookmarks.add_chapter_to_user_bookmarks(
                user,
                manga,
                chapter
            )

            response = {
                'status': 'success',
                'description': 'The chapter was successfully bookmarked.',
            }

    else:
        response = request_validation

    return JsonResponse(response, safe=False)

def is_chapter_in_user_bookmarks(request):
    request_validation = user_manga_session_request_validator.validate_request(request) 
    response = None
        
    if request_validation["status"] == "success":
        user = request_validation["user"]
        manga = request_validation["manga"]
        
        chapter_id = request.GET.get("chapter_id")
        chapter = Chapter.objects.get(
            id=chapter_id,
        )

        is_manga_chapter_in_user_bookmarks = user_bookmarks.is_chapter_in_user_bookmarks(
            user,
            manga,
            chapter
        )
    
        if is_manga_chapter_in_user_bookmarks:
            response = {
                'status': 'success',
                'is_manga_chapter_in_user_bookmarks': True,
                'description': 'The manga has been found the user\'s bookmarks.',
            }
        else:
            response = {
                'status': 'success',
                'is_manga_chapter_in_user_bookmarks': False,
                'description': 'The manga has not been found in the user\'s bookmarks.',
            }

    else:
        response = request_validation

    return JsonResponse(response, safe=False)

def remove_chapter_from_user_bookmarks(request):
    request_validation = user_manga_session_request_validator.validate_request(request)
    
    response = None
        
    if request_validation["status"] == "success":
        manga_id = request.GET.get("manga_id")

        user = user_session.get_authenticated_user(request)
        manga = Manga.objects.get(id=manga_id)

        chapter_id = request.GET.get("chapter_id")
        chapter = Chapter.objects.get(
            id=chapter_id,
        )
    
        is_manga_chapter_in_user_bookmarks = user_bookmarks.is_manga_chapter_in_user_bookmarks(
            user,
            manga,
            chapter,
        )

        if is_manga_chapter_in_user_bookmarks:
            success = user_bookmarks.remove_manga_chapter_from_user_bookmarks(
                user,
                manga,
                chapter
            )

            if success:
                response = {
                    "status": "success",
                    "description": "The chapter was removed from the user's bookmarks successfully."
                }
            else:
                response = {
                    "status": "failed",
                    "description": "Something doubly obscure went wrong with the system. It's our fault."
                }
        else:
            response = {
                'status': 'failed',
                'description': 'The chapter was not found in the user\'s bookmarks.',
            }
    else:
        response = request_validation

    return JsonResponse(response, safe=False)

def bookmarked_json(request):
    response = None

    try:
        manga_id = request.GET.get('manga_id')

        manga = Manga.objects.get(
            id=manga_id
        )
        
        user = user_session.get_authenticated_user(request)

        chapter = manga.bookmarked_by(user)

        if chapter:
            chapter = chapter.to_dict()

            response = {
                'status': 'success',
                'chapter': chapter,
            }

        else:
            response = {
                'status': 'bookmark_not_found',
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
