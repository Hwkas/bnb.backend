from django.urls import path

from . import api


urlpatterns = [
    path("", api.conversations_list, name="api-conversations-list"),
    path("<uuid:pk>/", api.conversations_detail, name="api-conversations-detail"),
    path(
        "start/<uuid:user_id>/",
        api.conversations_start,
        name="api-conversations-start",
    ),
]
