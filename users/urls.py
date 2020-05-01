from django.urls import path

from .views import html as account_html
from .views import json as account_json

urlpatterns = [
    path('', account_html.account_view),
    path('register', account_html.register_view),
    path('sign_in', account_html.sign_in_view),
    path('logout', account_html.logout_view),

    path('edit', account_json.edit),

    path('privacy_policy', account_html.privacy_policy)
]
