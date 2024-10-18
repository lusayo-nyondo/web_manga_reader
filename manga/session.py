import json

from django.core.paginator import Paginator
from django.db.models import Count

from manga.models import Manga, Chapter, Page, Author, Tag


# All logic that goes into handling manga in the backend
# without directly generating a response for the user
# and not being reliant on a particular user being logged in
# should go here.

def get_mangas_page_with_filters(
    page_number=1,
    items_per_page=24,
    authors=None,
    tags=None,
    order_by=None
):
        
    mangas = get_mangas_with_chapters_and_pages()

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
                manga_author__id=author_id
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

def get_mangas_with_chapters_and_pages():
    chapter_ids = Page.objects.values_list(
        'chapter_id',
        flat=True
    ).distinct()
    
    chapters = Chapter.objects.filter(
        id__in=chapter_ids
    )

    manga_ids = chapters.values_list(
        'manga_id',
        flat=True
    ).distinct()
    
    mangas = Manga.objects.filter(
        id__in=manga_ids
    )
    
    return mangas

def get_mangas_page(page_number, n, order_by):
    mangas = get_mangas_with_chapters_and_pages()

    mangas = mangas.order_by(
        order_by
    )

    manga_paginator = Paginator(
        mangas,
        n
    )

    mangas_page = manga_paginator.get_page(page_number)

    return mangas_page

def get_authors_page(page_number, n):
    authors = Author.objects.order_by('author_name')
    authors_paginator = Paginator(
        authors,
        n
    )

    authors_page = authors_paginator.get_page(page_number)

    return authors_page

def get_tags_page(page_number, n):
    tags = Tag.objects.order_by('tag_name')
    tags_paginator = Paginator(
        tags,
        n
    )

    tags_page = tags_paginator.get_page(page_number)

    return tags_page

