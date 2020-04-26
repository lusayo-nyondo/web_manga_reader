import json

from django.http import JsonResponse
from django.core import serializers, paginator

from .models import Post, Like

from users import session as user_session
from users.models import SiteUser

def post_comment(request):
    authenticated_user = user_session.get_authenticated_user(request)
    response = None

    if authenticated_user is not None:
        url = request.POST.get('location')
        text = request.POST.get('post')

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
    current_page = int(request.GET.get('current_page'))

    comments = Post.objects.filter(
        url=url,
    ).order_by(
        '-created_on'
    )

    count = len(comments)

    page_number = 1 if current_page <= 0 else current_page + 1

    comments_paginator = paginator.Paginator(
        comments,
        10
    )

    number_of_pages = comments_paginator.num_pages

    comments = comments_paginator.get_page(page_number)

    posts = json.loads(serializers.serialize('json', comments))
 
    for post, comment in zip(posts, comments):
        user = comment.user

        user_json = json.loads(
            serializers.serialize('json', [ user, ] )
        )

        likes_json = json.loads(
            serializers.serialize('json', comment.likes)
        )

        comments_json = json.loads(
            serializers.serialize('json', comment.comments)
        )

        user_likes_post = comment.does_user_like_post(user)

        post.setdefault('user', user_json)
        post.setdefault('likes', likes_json)
        post.setdefault('replies', comments_json)
        post.setdefault('user_likes_post', user_likes_post)

    response = {
        'posts': posts,
        'count': count,
        'page_number': page_number,
        'number_of_pages': number_of_pages,
    }

    return JsonResponse(response, safe=False)

def submit_like(request):
    response = None

    try:
        post_id = request.GET.get('post')
        user_id = request.GET.get('user')

        post = Post.objects.get(
            id=post_id,
        )

        user = SiteUser.objects.get(
            id=user_id,
        )

        try:
            like = Like.objects.get(
                post=post,
                user=user
            )

            like.delete()
            
            likes = post.likes
            likes = len(likes)

            response = {
                'status': 'success',
                'description': 'You have unliked this foul pestilence.',
                'likes': likes,
            }
        except Like.DoesNotExist:
            like = Like(
                post=post,
                user=user
            )

            like.save()

            likes = post.likes
            likes = len(likes)

            response = {
                'status': 'success',
                'description': 'The like hath been updated successfully.',
                'likes': likes,
            }
    except KeyError:
        response = {
            'status': 'fatal',
            'description': 'The request had missing keys. Either post or user.',
        }
    except Post.DoesNotExist:
        response = {
            'status': 'fatal',
            'description': 'No post exists with the ID provided.'
        }
    except SiteUser.DoesNotExist:
        response = {
            'status': 'fatal',
            'description': 'No user exists with the ID provided.'
        }

    return JsonResponse(response, safe=False)
