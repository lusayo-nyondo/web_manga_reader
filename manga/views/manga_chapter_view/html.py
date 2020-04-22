from django.http import HttpResponse
from django.template import loader

from manga.models import Manga, Chapter, Page

from users import session as user_session

from user_manga_integration.session import bookmarks as user_bookmarks
from user_manga_integration.session import history as user_history

def manga_chapter_view(request, manga_id=0, chapter_number=0):  
    manga = Manga.objects.get(
        id=manga_id
    )

    chapters = Chapter.objects.filter(
        manga_id=manga_id
    )

    chapter = chapters.get(
        chapter_number=chapter_number,
    )

    pages = Page.objects.filter(
        chapter_id=chapter.id
    )

    context = {
        'chapter': chapter,
        'pages': pages,
        'manga': manga,
        'chapters': chapters,
        'mode': None
    }

    context = user_session.attach_active_user_to_context(context, request)

    user = user_session.get_authenticated_user(request)
    
    is_manga_chapter_in_bookmarks = user_bookmarks.is_manga_chapter_in_user_bookmarks(
        user=user,
        manga=manga,
        chapter=chapter,
    )

    context['is_manga_chapter_in_user_bookmarks'] = is_manga_chapter_in_bookmarks

    template = loader.get_template('manga/modules/manga_chapter_view.dtl.html')

    try:
        mode = request.GET.get('mode')
        context['mode'] = mode
    except KeyError:
        try:
            mode = request.COOKIES['mode']
            context['mode'] = mode
        except KeyError:
            context['mode'] = 'single_page'

    response = HttpResponse(template.render(context, request))

    response.set_cookie('mode', mode)

    if user:
        user_history.add_chapter_to_user_history(
            user=user,
            manga=manga,
            chapter=chapter,
        )
    
    return response
