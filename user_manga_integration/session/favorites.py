import json


from django.db.models import Count

from django.core.paginator import Paginator

from django.contrib.auth.decorators import login_required

from users import session as user_session
from users.models import SiteUser

from manga.models import Manga, Chapter

from user_manga_integration.models import UserMangaRating

def get_favorite_mangas(
    user,
    order_by='-updated_on'
):
    return get_user_favorites(
        user=user,
    )

def get_favorites_page(user, page_number, items_per_page, order_by):
    mangas = get_favorite_mangas(
        user=user,
        order_by=order_by
    )

    favorites_manga_paginator = Paginator(
        mangas,
        items_per_page
    )

    favorites_manga_page = favorites_manga_paginator.get_page(page_number)

    return favorites_manga_page

def get_favorites_page_with_filters(
    user,
    page_number=1,
    items_per_page=24,
    authors=None,
    tags=None,
    order_by=None
):
    mangas = get_favorite_mangas(
        user=user,
        order_by=order_by
    )

    if tags is not None:
        tags = json.loads(tags)
        tags = tags['tags']
    
        for tag_id in tags:
            mangas = mangas.filter(
                tags__id=str(tag_id)
            )

    if authors is not None:
        authors = json.loads(authors)
        authors = authors['authors']

        for author_id in authors:
            mangas = mangas.filter(
                manga_author__id=str(author_id)
            )

    if order_by:
        if order_by == 'chapter_count' or order_by == '-chapter_count':
            mangas = mangas.annotate(
                chapter_count=Count('chapter')
            ).order_by(
                order_by
            )
        else:
            mangas = mangas.order_by(order_by)

    paginator = None

    if items_per_page:
        items_per_page = int(items_per_page)
        paginator = Paginator(mangas, items_per_page)
        mangas = paginator.get_page(page_number)

    return mangas

def get_user_favorites(user):
    user_favorites_entries = UserMangaRating.objects.filter(
        user=user,
    ).order_by('-rating')

    manga_ids = user_favorites_entries.values('manga_id')

    user_favorites_mangas = Manga.objects.filter(
        id__in=manga_ids,
    )

    return user_favorites_mangas

def is_manga_in_user_favorites(user, manga):
    try:
        favorites_entry = UserMangaRating.objects.get(
            user=user,
            manga=manga,
        )

        return True
    except UserMangaRating.DoesNotExist:
        return False


def remove_manga_from_user_favorites(user, manga):
    try:
        favorites_entry = UserMangaRating.objects.get(
            manga=manga,
            user=user,
        )

        favorites_entry.delete()

    except UserMangaRating.DoesNotExist:
        return False
    return True
