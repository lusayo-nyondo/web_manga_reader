import json

from django.db.models import Count

from django.core.paginator import Paginator

from django.contrib.auth.decorators import login_required

from users import session as user_session
from users.models import SiteUser

from manga.models import Manga, Chapter

from user_manga_integration.models import UserChapterBookmarkEntry

def get_bookmarked_mangas(
    user,
    order_by='-updated_on'
):
    bookmarks_entries = get_user_bookmarks(user).values_list(
        'chapter_id',
        flat=True,
    )

    chapters = Chapter.objects.filter(
        id__in=bookmarks_entries,
    )

    manga_ids = chapters.all().values('manga_id')

    mangas = Manga.objects.filter(
        id__in=manga_ids
    )

    return mangas

def get_bookmarks_page(user, page_number, items_per_page, order_by):
    mangas = get_bookmarked_mangas(
        user=user,
        order_by=order_by,
    )

    bookmarked_manga_paginator = Paginator(
        mangas,
        items_per_page
    )

    bookmarked_manga_page = bookmarked_manga_paginator.get_page(page_number)

    return bookmarked_manga_page


def get_bookmarks_page_with_filters(
    user,
    page_number=1,
    items_per_page=24,
    authors=None,
    tags=None,
    order_by=None
):
    mangas = get_bookmarked_mangas(
        user=user,
        order_by=order_by,
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

def get_user_bookmarks(user):
    user_bookmarks = UserChapterBookmarkEntry.objects.filter(
        user=user,
        is_manually_assigned=True,
    )
    return user_bookmarks

def add_chapter_to_user_bookmarks(user, manga, chapter):
    if is_manga_chapter_in_user_bookmarks(
        user=user,
        manga=manga,
        chapter=chapter):
        return False
    
    # The boomark entry doubles for a manga reading history entry.
    # If it is manually assigned, it means that the bookmark should
    # be considered an active bookmark that the user is concerned about explicitly.

    # If it is not manually assigned, it will be considered a history entry.
    bookmark_entry = UserChapterBookmarkEntry.objects.get_or_create(
        user=user,
        manga=manga,
        chapter=chapter,
    )[0]

    bookmark_entry.is_manually_assigned = True

    bookmark_entry.save()
    
def is_manga_chapter_in_user_bookmarks(user, manga, chapter):
    try:
        bookmark_entry = UserChapterBookmarkEntry.objects.get(
            user=user,
            manga=manga,
            chapter=chapter,
            is_manually_assigned=True,
        )

        return True
    except UserChapterBookmarkEntry.DoesNotExist:
        return False

def remove_manga_chapter_from_user_bookmarks(user, manga, chapter):
    try:
        bookmark_entry = UserChapterBookmarkEntry.objects.get(
            manga=manga,
            user=user,
            chapter=chapter,
            is_manually_assigned=True,
        )

        bookmark_entry.is_manually_assigned = False

        bookmark_entry.save()
    except UserChapterBookmarkEntry.DoesNotExist:
        return False
    return True
