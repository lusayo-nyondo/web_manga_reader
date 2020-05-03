import json

from django.http import JsonResponse
from django.core import serializers, paginator
from django.core.exceptions import RequestDataTooBig

from .models import Post, Like

from users import session as user_session
from users.models import SiteUser

from config.settings import DATA_UPLOAD_MAX_MEMORY_SIZE

def post_comment(request):
    try:
        authenticated_user = user_session.get_authenticated_user(request)
        response = None

        if authenticated_user is not None:
            url = request.POST.get('location')
            text = request.POST.get('post')

            if int(request.META.get('CONTENT_LENGTH')) > DATA_UPLOAD_MAX_MEMORY_SIZE:
                response = {
                    'status': 'failed',
                    'description': 'Your post is too large for our teeny weeny database.'
                }
            else:    
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
    except RequestDataTooBig:
        response = {
            'status': 'failed',
            'description': 'Your post is too large for our teeny weeny database.'
        }
    return JsonResponse(response, safe=False)

def fetch_comments(request):
    url = request.GET.get('url')
    current_page = int(request.GET.get('current_page'))

    response = get_posts_responding_to(url, current_page, None)

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

def submit_reply(request):
    response = None

    try:
        post_id = request.POST.get('post')
        user_id = request.POST.get('user')
        reply = request.POST.get('reply')
        url = request.POST.get('location')

        if int(request.META.get('CONTENT_LENGTH')) > DATA_UPLOAD_MAX_MEMORY_SIZE:
            response = {
                'status': 'failed',
                'description': 'Your post is too large for our teeny weeny database.'
            }
        else:
            post = Post.objects.get(
                id=post_id,
            )

            user = SiteUser.objects.get(
                id=user_id,
            )

            reply_obj = Post(
                url=url,
                user=user,
                responding_to=post,
                text=reply
            )

            reply_obj.save()

            response = {
                'status': 'success',
                'description': 'Your response hath been accepted by Akasha.',
            }
    except KeyError:
        response = {
            'status': 'fatal',
            'description': 'The request had missing keys. Either post, user, reply or location.',
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

def get_posts_responding_to(url, current_page, post):
    post_objs = Post.objects.filter(
        url=url,
        responding_to=post
    ).order_by(
        '-created_on'
    )

    count = len(post_objs)

    page_number = 1 if current_page <= 0 else current_page + 1

    post_objs_paginator = paginator.Paginator(
        post_objs,
        10
    )

    number_of_pages = post_objs_paginator.num_pages

    post_objs = post_objs_paginator.get_page(page_number)

    posts_json = json.loads(serializers.serialize('json', post_objs))
 
    for post_json, post_obj in zip(posts_json, post_objs):
        set_post_properties(post_json, post_obj)

        replies = post_obj.comments
        replies_json = json.loads(
            serializers.serialize('json', replies)
        )

        for reply_json, reply_obj in zip(replies_json, replies):
            set_post_properties(reply_json, reply_obj)

        post_json.setdefault('replies', replies_json)

    response = {
        'posts': posts_json,
        'count': count,
        'page_number': page_number,
        'number_of_pages': number_of_pages,
    }

    return response

def set_post_properties(post_json, post_obj):
    user = post_obj.user

    user_json = json.loads(
        serializers.serialize('json', [ user, ] )
    )

    user_likes_post = post_obj.does_user_like_post(user)

    likes_json = json.loads(
        serializers.serialize('json', post_obj.likes)
    )

    post_json.setdefault('user', user_json)
    post_json.setdefault('likes', likes_json)
    post_json.setdefault('user_likes_post', user_likes_post)