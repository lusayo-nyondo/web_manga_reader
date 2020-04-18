
import json

from django.core import serializers
from django.http import JsonResponse
from django.db.models import Count, Q

from manga import session as manga_session
from manga.models import Tag, Author, Chapter
from manga.views.manga_list import queryset

from users import session as user_session

from user_manga_integration.session import watchlist as user_watchlist
from user_manga_integration.session import bookmarks as user_bookmarks
from user_manga_integration.session import history as user_history
from user_manga_integration.session import favorites as user_favorites

# Method for applying filters
def manga_page_json(request, page_number):
    mangas = queryset.get_mangas_page_with_filters(
        request,
        page_number
    )

    json_response = json.loads(serializers.serialize('json', mangas))
    
    for manga_json, manga_model in zip(json_response, mangas):
        manga_json['latest_chapter'] = manga_model.latest_chapter.chapter_number
        
        tags = Tag.objects.filter(
            id__in=manga_model.tags.all()
        )

        tags_json = json.loads(serializers.serialize('json', tags))

        manga_json['tags'] = tags_json

        if manga_model.history_entry:
            manga_json['history_entry'] = json.loads(serializers.serialize('json', [ manga_model.history_entry ]))
            chapter = Chapter.objects.get(id=manga_model.history_entry.chapter.id)
            manga_json['history_entry'][0]['chapter'] = json.loads(serializers.serialize('json', [ chapter ]))

    context = {
        'num_pages': mangas.paginator.num_pages,
        'mangas': json_response,
    }

    return JsonResponse(context, safe=False)

def author_page_json(request, page_number):
    items_per_page = request.GET.get('items_per_page')

    if not items_per_page:
        return

    authors_page = manga_session.get_authors_page(page_number, items_per_page)
    authors_json = json.loads(serializers.serialize('json', authors_page))

    return JsonResponse(authors_json, safe=False)

def tag_page_json(request, page_number):
    items_per_page = request.GET.get('items_per_page')

    if not items_per_page:
        return

    tags_page = manga_session.get_tags_page(page_number, items_per_page)
    tags_json = json.loads(serializers.serialize('json', tags_page))

    return JsonResponse(tags_json, safe=False)

# Method for searching for a particular manga name
def manga_list_json(request):
    manga_list = manga_session.get_mangas_with_chapters_and_pages()
    search_term = request.GET.get('search_term')
    search_term = search_term.lower()

    if search_term is not None:
        manga_list = manga_list.filter(
            manga_name__icontains=search_term
        ).order_by(
            'manga_name'
        )[:10]
    
        json_response = serializers.serialize('json', manga_list)
    
        return JsonResponse(json_response, safe=False)

    response = {}

    return JsonResponse(response, safe=False)

def tag_list_json(request):
    search_term = request.GET.get('search_term')
    search_term = search_term.lower()

    if search_term is not None:
        tag_list = Tag.objects.filter(
            tag_name__icontains=search_term
        ).order_by(
            'tag_name'
        )[:10]

        json_response = serializers.serialize('json', tag_list)

        return JsonResponse(json_response, safe=False)

    response = {}

    return JsonResponse(response, safe=False)

def author_list_json(request):
    search_term = request.GET.get('search_term')
    search_term = search_term.lower()

    if search_term is not None:
        author_list = Author.objects.filter(
            author_name__icontains=search_term
        ).order_by(
            'author_name'
        )[:10]

        json_response = serializers.serialize('json', author_list)

        return JsonResponse(json_response, safe=False)

    response = {}

    return JsonResponse(response, safe=False)