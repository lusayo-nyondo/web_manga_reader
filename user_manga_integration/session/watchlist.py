import json

from django.db.models import Count

from django.core.paginator import Paginator

from django.contrib.auth.decorators import login_required

from users import session as user_session
from users.models import SiteUser

from manga.models import Manga

from user_manga_integration.models import UserMangaWatchlistEntry

def get_watchlist_mangas(
    user,
    order_by
):
    watchlist_entries = get_user_watchlist(user).values_list(
        'manga_id',
        flat=True,
    )

    mangas = Manga.objects.filter(
        id__in=watchlist_entries,
    ).order_by(
        order_by
    )

    return mangas

def get_watchlist_page(user, page_number, items_per_page, order_by):
    mangas = get_watchlist_mangas(
        user,
        order_by
    )

    manga_paginator = Paginator(
        mangas,
        items_per_page
    )

    mangas_page = manga_paginator.get_page(page_number)

    return mangas_page

def get_watchlist_page_with_filters(
    user,
    page_number=1,
    items_per_page=24,
    authors=None,
    tags=None,
    order_by=None
):
    mangas = get_watchlist_mangas(
        user,
        order_by
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

def get_user_watchlist(user):
    user_watchlist = UserMangaWatchlistEntry.objects.filter(
        user=user,
    )

    return user_watchlist

def add_manga_to_user_watchlist(user, manga):
    
    if is_manga_in_user_watchlist(user,manga):
        return False
    
    watchlist_entry = UserMangaWatchlistEntry.objects.create(
        manga=manga,
        user=user,
    )

    if watchlist_entry:
        return True

    return False

def is_manga_in_user_watchlist(user, manga):
    try:
        watchlist_entry = UserMangaWatchlistEntry.objects.get(
            manga=manga,
            user=user,
        )

        return True

    except UserMangaWatchlistEntry.DoesNotExist:
        return False

def remove_manga_from_user_watchlist(user, manga):
    try:
        UserMangaWatchlistEntry.objects.get(
            manga=manga,
            user=user,
        ).delete()
    except UserMangaWatchlistEntry.DoesNotExist:
        return False
    return True
