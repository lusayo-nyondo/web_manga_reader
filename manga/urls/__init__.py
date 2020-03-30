from .manga_chapter_view import \
    html as manga_chapter_html, \
    json as manga_chapter_json

from .manga_chapters_overview import \
    html as manga_chapters_html, \
    json as manga_chapters_json

from .manga_list import \
    html as manga_list_html, \
    json as manga_list_json

urlpatterns = list()

urlpatterns += manga_chapter_html.urlpatterns
urlpatterns += manga_chapter_json.urlpatterns

urlpatterns += manga_chapters_html.urlpatterns
urlpatterns += manga_chapters_json.urlpatterns


urlpatterns += manga_list_html.urlpatterns
urlpatterns += manga_list_json.urlpatterns