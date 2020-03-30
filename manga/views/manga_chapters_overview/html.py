from django.http import HttpResponse
from django.template import loader
from django.db.models import Count

from manga.models import Manga, Chapter, Author, Tag

from users import session as user_session
from user_manga_integration.session import watchlist as user_watchlist

def manga_chapters_overview(request, manga_id=0):
    manga = Manga.objects.get(
        id=manga_id
    )

    chapters = Chapter.objects.filter(
        manga_id=manga_id
    )

    valid_ratings = manga.valid_ratings
    rating = None

    user = user_session.get_authenticated_user(request)

    if user:
        rating = manga.rating_by(user)
    else:
        rating = manga.rating

    authors = manga.manga_author.all()
    tags = manga.tags.all()
    translators = manga.manga_translator.all()
    
    manga_same_author = Manga.objects.filter(
        manga_author__in=authors,
    ).exclude(
        id=manga.id
    )

    manga_same_tags = parents = Manga.objects.annotate(
        count=Count('tags')
    ).filter(
        count=len(tags)
    ).exclude(
        id=manga.id
    )

    for tag in tags:
        manga_same_tags = manga_same_tags.filter(
            tags__id=tag.id
        )
    
    alternate_names = manga.alternate_names.all()
    translators = manga.manga_translator.all()

    context = {
        'manga': manga,
        'chapters': chapters,
        'rating': rating,
        'valid_ratings': valid_ratings,
        'tags': tags,
        'authors': authors,
        'translators': translators,
        'alternate_names': alternate_names,
        'manga_same_author': manga_same_author,
        'manga_same_tags': manga_same_tags,
    }

    user = user_session.get_authenticated_user(request)

    is_manga_in_watchlist = user_watchlist.is_manga_in_user_watchlist(
        user=user,
        manga=manga,
    )

    context['is_manga_in_watchlist'] = is_manga_in_watchlist

    template = loader.get_template('manga/modules/manga_chapters_overview.dtl.html')

    return HttpResponse(template.render(context, request))
