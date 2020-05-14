from django.core import serializers
from django.core.paginator import Paginator

from django.shortcuts import render, loader

from django.http import HttpResponse, JsonResponse

from django.contrib.auth.decorators import login_required

from manga import session as manga_session
from manga.models import Manga

from users import session as user_session
from users.models import SiteUser

from user_manga_integration.session import bookmarks as user_bookmarks

# Create your views here.

@login_required
def manga_list_bookmarks_view(request):
    authors_page = manga_session.get_authors_page(1, 10)
    tags_page = manga_session.get_tags_page(1, 10)

    active_user = user_session.get_authenticated_user(request)
    
    order_by = request.GET.get('order_by')

    if order_by is None:
        order_by = 'manga_name'

    bookmarked_mangas = user_bookmarks.get_bookmarks_page(active_user, 1, 12, order_by)

    template = loader.get_template('manga/modules/manga_list.dtl.html')

    context = {
        'sections': (
            {
                'section_id': 'bookmarks',
                'section_name': 'Bookmarks',
                'section_description': 'This is where you can keep up with your reading progress.',
                'section_order': 'manga_name',
                'section_items_per_page': 12,
                'section_content': bookmarked_mangas,
                'pages': range(1, bookmarked_mangas.paginator.num_pages + 1)
            },
        ),
        'filterable_section': 'bookmarks',
        'filterable_section_items_per_page': 12,
        'all_authors': authors_page,
        'author_pages': range(1, authors_page.paginator.num_pages + 1),
        'all_tags': tags_page,
        'tag_pages': range(1, tags_page.paginator.num_pages + 1),
    }

    context = user_session.attach_active_user_to_context(context, request)

    return HttpResponse(template.render(context, request))
