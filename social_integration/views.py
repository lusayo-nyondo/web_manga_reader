import json

from django.http import JsonResponse
from django.core import serializers

from .models import Post

from users import session as user_session

def post_comment(request):
    authenticated_user = user_session.get_authenticated_user(request)
    response = None

    if authenticated_user is not None:
        url = request.GET.get('location')
        text = request.GET.get('post')

        post = Post(
            user=authenticated_user,
            url=url,
            text=text
        )

        post.save()

        response = {
            'status': 'success',
            'description': 'The post has been added successfully.',
        }
    else:
        response = {
            'status': 'failed',
            'description': 'You need to login to get this functionality.',
        }

    return JsonResponse(response, safe=False)

def fetch_comments(request):
    url = request.GET.get('url')

    comments = Post.objects.filter(
        url=url,
    ).order_by(
        '-created_on'
    )

    posts = json.loads(serializers.serialize('json', comments))

    response = {
        'posts': posts,
    }

    return JsonResponse(response, safe=False)
