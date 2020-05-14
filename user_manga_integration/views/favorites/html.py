from django.core import serializers
from django.core.paginator import Paginator

from django.shortcuts import render, loader

from django.http import HttpResponse, JsonResponse

from django.contrib.auth.decorators import login_required

from manga import session as manga_session
from manga.models import Manga

from users import session as user_session
from users.models import SiteUser

from user_manga_integration.session import favorites as user_favorites

# Create your views here.

@login_required
def manga_list_favorites_view(request):
    authors_page = manga_session.get_authors_page(1, 10)
    tags_page = manga_session.get_tags_page(1, 10)

    active_user = user_session.get_authenticated_user(request)
    
    order_by = request.GET.get('order_by')

    if order_by is None:
        order_by = 'updated_on'

    favorites_mangas = user_favorites.get_favorites_page(active_user, 1, 12, order_by)

    template = loader.get_template('manga/modules/manga_list.dtl.html')

    context = {
        'sections': (
            {
                'section_id': 'favorites',
                'section_name': 'My Favorites',
                'section_description': 'This is where manga that you have rated goes, just to help you keep up with what caught your attention generally.',
                'section_order': 'updated_on',
                'section_items_per_page': 12,
                'section_content': favorites_mangas,
                'pages': range(1, favorites_mangas.paginator.num_pages + 1)
            },
        ),
        'filterable_section': 'favorites',
        'filterable_section_items_per_page': 12,
        'all_authors': authors_page,
        'author_pages': range(1, authors_page.paginator.num_pages + 1),
        'all_tags': tags_page,
        'tag_pages': range(1, tags_page.paginator.num_pages + 1),
    }

    context = user_session.attach_active_user_to_context(context, request)

    return HttpResponse(template.render(context, request))
