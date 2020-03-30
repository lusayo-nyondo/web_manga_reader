import json

from django.db.models import Count

from django.core.paginator import Paginator

from django.contrib.auth.decorators import login_required

from users import session as user_session
from users.models import SiteUser

from manga.models import Manga, Chapter

from user_manga_integration.models import UserChapterBookmarkEntry

def get_history_mangas(
    user,
    order_by='-updated_on'
):
    history_entries = get_user_history(user).values_list(
        'chapter_id',
        flat=True,
    )

    chapters = Chapter.objects.filter(
        id__in=history_entries,
    )

    manga_ids = chapters.all().values('manga_id')

    mangas = Manga.objects.filter(
        id__in=manga_ids
    )

    return mangas

def get_history_page(user, page_number, items_per_page, order_by):
    mangas = get_history_mangas(
        user=user,
        order_by=order_by
    )

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
    user_history = UserChapterBookmarkEntry.objects.filter(
        user=user,
        is_manually_assigned=False,
    ).order_by('-updated_on')

    return user_history

def add_chapter_to_user_history(user, manga, chapter):
    # The boomark entry doubles for a manga reading history entry.
    # If it is manually assigned, it means that the history should
    # be considered an active history that the user is concerned about explicitly.

    # If it is not manually assigned, it will be considered a history entry.
    # Since the model assumes is_manually_assigned is False by default, unless
    # the user explicitly bookmarks the chapter, this won't change.

    # If the user does bookmark the chapter, we save the model.

    # This makes sure that we update the updated_on field regardless of
    # whether it is a bookmark entry or a history entry.

    history_entry = UserChapterBookmarkEntry.objects.get_or_create(
        user=user,
        manga=manga,
        chapter=chapter
    )[0]

    history_entry.save()

def is_manga_chapter_in_user_history(user, manga, chapter):
    try:
        history_entry = UserChapterBookmarkEntry.objects.get(
            user=user,
            manga=manga,
            chapter=chapter,
            is_manually_assigned=False,
        )

        return True
    except UserChapterBookmarkEntry.DoesNotExist:
        return False


def remove_manga_chapter_from_user_history(user, manga, chapter):
    try:
        history_entry = UserChapterBookmarkEntry.objects.get(
            manga=manga,
            user=user,
            chapter=chapter,
            is_manually_assigned=False,
        )

        history_entry.is_manually_assigned = False

        history_entry.save()
    except UserChapterBookmarkEntry.DoesNotExist:
        return False
    return True
