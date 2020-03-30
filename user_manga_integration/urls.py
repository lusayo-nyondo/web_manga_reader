from django.urls import path

from user_manga_integration.views.dashboard import html as dashboard_html

from user_manga_integration.views.watchlist import html as watchlist_html
from user_manga_integration.views.bookmarks import html as bookmarks_html
from user_manga_integration.views.history import html as history_html
from user_manga_integration.views.favorites import html as favorites_html

from user_manga_integration.views.watchlist import json as watchlist_json
from user_manga_integration.views.bookmarks import json as bookmarks_json
from user_manga_integration.views.history import json as history_json
from user_manga_integration.views.ratings import json as ratings_json

urlpatterns = [
    path('', dashboard_html.user_dashboard),
    path('user_dashboard', dashboard_html.user_dashboard),
    
    #### START WATCHLIST URLS
    path('my_watchlist', watchlist_html.manga_list_watchlist_view),
    
    path('add_manga_to_watchlist', watchlist_json.add_manga_to_user_watchlist),
    path('is_manga_in_watchlist', watchlist_json.is_manga_in_user_watchlist),
    path('remove_manga_from_watchlist', watchlist_json.remove_manga_from_user_watchlist),
    #### END WATCHLIST URLS

    ### START BOOKMARK URLS
    path('my_bookmarks', bookmarks_html.manga_list_bookmarks_view),

    path('add_chapter_to_bookmarks', bookmarks_json.add_chapter_to_user_bookmarks),
    path('is_chapter_in_bookmarks', bookmarks_json.is_chapter_in_user_bookmarks),
    path('remove_chapter_from_bookmarks', bookmarks_json.remove_chapter_from_user_bookmarks),

    path('bookmarked_json', bookmarks_json.bookmarked_json),
    ### END BOOKMARK URLS

    ### START HISTORY URLS
    path('my_history', history_html.manga_list_history_view),

    path('last_read_json', history_json.last_read_json),
    ### END HISTORY URLS

    ### START RATING RELATED URLS
    path('my_favorites', favorites_html.manga_list_favorites_view),
    
    path('submit_rating', ratings_json.submit_rating),
    ### END RATING RELATED URLS
]


### START MANGA COLLECTION URLS
"""path('add_manga_collection', json.add_manga_to_user_manga_collection),
path('is_manga_in_collection', json.is_manga_in_user_manga_collection),
path('remove_manga_collection', json.remove_user_manga_collection),
path('modify_manga_colletion', json.modify_user_manga_collection),
path('add_mangas_to_collection', json.add_mangas_to_user_manga_collection),
path('remove_mangas_from_collection', json.remove_mangas_from_user_manga_collection),
### END MANGA COLLECTION URLS
"""
### START MANGA TAGS SUBSCRIPTION URLS
"""path('add_manga_tags_subscription', json.add_manga_tags_subscription),
path('is_subscribed_to_manga_tags', json.is_subscribed_to_manga_tags),
path('remove_manga_tags_subscription', json.remove_manga_tags_subscription),
path('modify_manga_tags_subscription', json.remove_manga_tags_subscription),
path('add_tags_to_manga_tags_subscription', json.add_tags_to_manga_tags_subscription),
path('remove_tags_from_manga_tags_subscription', json.remove_tags_from_manga_tags_subscription),
### END MANGA TAGS SUBSCRIPTION URLS
"""