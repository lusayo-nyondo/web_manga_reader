from manga import session as manga_session

from users import session as user_session

from user_manga_integration.session import watchlist as user_watchlist
from user_manga_integration.session import bookmarks as user_bookmarks
from user_manga_integration.session import history as user_history
from user_manga_integration.session import favorites as user_favorites

# Method for applying filters
def get_mangas_page_with_filters(request, page_number):
    items_per_page = request.GET.get('items_per_page')
    tags = request.GET.get('tags')
    authors = request.GET.get('authors')
    order_by = request.GET.get('order_by')
    section_id = request.GET.get('section_id')

    mangas = None

    if section_id == 'watchlist':
        user = user_session.get_authenticated_user(request)
        mangas = user_watchlist.get_watchlist_page_with_filters(
            user=user,
            page_number=page_number,
            items_per_page=items_per_page,
            authors=authors,
            tags=tags,
            order_by=order_by
        )
    elif section_id == 'bookmarks':
        user = user_session.get_authenticated_user(request)
        mangas = user_bookmarks.get_bookmarks_page_with_filters(
            user=user,
            page_number=page_number,
            items_per_page=items_per_page,
            authors=authors,
            tags=tags,
            order_by=order_by
        )
    elif section_id == 'history':
        user = user_session.get_authenticated_user(request)
        mangas = user_history.get_history_page_with_filters(
            user=user,
            page_number=page_number,
            items_per_page=items_per_page,
            authors=authors,
            tags=tags,
            order_by=order_by
        )
    elif section_id == 'favorites':
        user = user_session.get_authenticated_user(request)
        mangas = user_favorites.get_favorites_page_with_filters(
            user=user,
            page_number=page_number,
            items_per_page=items_per_page,
            authors=authors,
            tags=tags,
            order_by=order_by
        )
    else:
        mangas = manga_session.get_mangas_page_with_filters(
            page_number=page_number,
            items_per_page=items_per_page,
            authors=authors,
            tags=tags,
            order_by=order_by
        )

    return mangas