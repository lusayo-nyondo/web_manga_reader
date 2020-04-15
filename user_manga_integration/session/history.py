import json

from django.db.models import Count, F, Subquery, OuterRef

from django.core.paginator import Paginator

from django.contrib.auth.decorators import login_required

from users import session as user_session
from users.models import SiteUser

from manga.models import Manga, Chapter

from user_manga_integration.models import UserChapterHistoryEntry

def get_history_mangas(
    user,
    order_by='-updated_on'
):
    history_entries = get_user_history(user)
    history_entries.order_by(order_by)

    mangas = list()

    for history_entry in history_entries:
        manga = Manga.objects.get(
            id=history_entry.manga.id
        )

        manga.history_entry = history_entry
        
        mangas.append(manga)
    
    return mangas

def get_history_page(user, page_number, items_per_page, order_by):
    mangas = get_history_mangas(
        user=user,
        order_by=order_by
    )

    print(mangas)

    history_manga_paginator = Paginator(
        mangas,
        items_per_page
    )

    history_manga_page = history_manga_paginator.get_page(page_number)

    return history_manga_page

def get_history_page_with_filters(
    user,
    page_number=1,
    items_per_page=24,
    authors=None,
    tags=None,
    order_by=None
):
    mangas = get_history_mangas(
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

def get_user_history(user):
    user_history = UserChapterHistoryEntry.objects.filter(
        user=user,
    ).order_by(
        '-updated_on'
    )

    return user_history

def add_chapter_to_user_history(user, manga, chapter):
    history_entry = UserChapterHistoryEntry.objects.create(
        user=user,
        manga=manga,
        chapter=chapter
    )

    history_entry.save()

def is_manga_chapter_in_user_history(user, manga, chapter):
    try:
        history_entry = UserChapterHistoryEntry.objects.get(
            user=user,
            manga=manga,
            chapter=chapter,
            is_manually_assigned=False,
        )

        return True
    except UserChapterHistoryEntry.DoesNotExist:
        return False


def remove_manga_chapter_from_user_history(user, manga, chapter):
    try:
        history_entry = UserChapterHistoryEntry.objects.get(
            manga=manga,
            user=user,
            chapter=chapter,
        )

        history_entry.is_manually_assigned = False

        history_entry.save()
    except UserChapterHistoryEntry.DoesNotExist:
        return False
    return True
