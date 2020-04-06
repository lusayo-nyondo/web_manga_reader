import json

from django.http import HttpResponse
from django.template import loader

from users import session as user_session

from manga import session as manga_session
from manga.models import Tag
from manga.views.manga_list import queryset

def index(request):
    return manga_list_default_view(request)

def manga_list_all_view(request):
    authors_page = manga_session.get_authors_page(1, 10)
    tags_page = manga_session.get_tags_page(1, 10)

    manga_list = manga_session.get_mangas_page(1, 24, 'updated_on')

    template = loader.get_template('manga/modules/manga_list.dtl.html')
    context = {
        'sections': (
            {
                'section_id': 'manga_list',
                'section_name': 'Manga List',
                'section_order': 'manga_name',
                'section_items_per_page': 24,
                'section_content': manga_list,
                'pages': range(1, manga_list.paginator.num_pages + 1)
            },
        ),
        'filterable_section': 'manga_list',
        'filterable_section_items_per_page': 24,
        'all_authors': authors_page,
        'author_pages': range(1, authors_page.paginator.num_pages + 1),
        'all_tags': tags_page,
        'tag_pages': range(1, tags_page.paginator.num_pages + 1)
    }

    return HttpResponse(template.render(context, request))

def manga_list_filtered_view(request, page_number):
    authors_page = manga_session.get_authors_page(1, 10)
    tags_page = manga_session.get_tags_page(1, 10)

    manga_list = queryset.get_mangas_page_with_filters(
        request,
        page_number
    )

    tags = request.GET.get('tags')

    if tags:
        tags = json.loads(tags)
        tags = tags['tags']

    active_tags = Tag.objects.filter(
        id__in=tags,
    )

    template = loader.get_template('manga/modules/manga_list.dtl.html')
    context = {
        'sections': (
            {
                'section_id': 'manga_list',
                'section_name': 'Manga List',
                'section_order': 'manga_name',
                'section_items_per_page': 24,
                'section_content': manga_list,
                'pages': range(1, manga_list.paginator.num_pages + 1)
            },
        ),
        'filterable_section': 'manga_list',
        'filterable_section_items_per_page': 24,
        'all_authors': authors_page,
        'author_pages': range(1, authors_page.paginator.num_pages + 1),
        'all_tags': tags_page,
        'tag_pages': range(1, tags_page.paginator.num_pages + 1),
        'active_tags': active_tags
    }

    return HttpResponse(template.render(context, request))

def manga_list_default_view(request):
    authors_page = manga_session.get_authors_page(1, 10)
    tags_page = manga_session.get_tags_page(1, 10)

    latest_manga_list = manga_session.get_mangas_page(1, 12, '-added_on')
    popular_manga_list = manga_session.get_mangas_page(1, 12, '-views')
    recently_updated_list = manga_session.get_mangas_page(1, 12, '-updated_on')

    template = loader.get_template('manga/modules/manga_list.dtl.html')
    context = {
        'sections': (
            {
                'section_id': 'newly_added',
                'section_name': 'Newly Added',
                'section_order': '-added_on',
                'section_items_per_page': 12,
                'section_content': latest_manga_list,
                'pages': range(1, latest_manga_list.paginator.num_pages + 1)
            },{
                'section_id': 'recently_updated',
                'section_name': 'Recently Updated',
                'section_order': '-updated_on',
                'section_items_per_page': 12,
                'section_content': recently_updated_list,
                'pages': range(1, recently_updated_list.paginator.num_pages + 1),
            },{
                'section_id': 'popular_manga',
                'section_name': 'Popular Manga',
                'section_order': '-views',
                'section_items_per_page': 12,
                'section_content': popular_manga_list,
                'pages': range(1, popular_manga_list.paginator.num_pages + 1),
            }
        ),
        'filterable_section': 'None',
        'filterable_section_items_per_page': 0,
        'all_authors': authors_page,
        'author_pages': range(1, authors_page.paginator.num_pages + 1),
        'all_tags': tags_page,
        'tag_pages': range(1, tags_page.paginator.num_pages + 1),
    }

    context = user_session.attach_active_user_to_context(context, request)

    return HttpResponse(template.render(context, request))