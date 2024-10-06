from django.urls import path

from dj_rest_auth.jwt_auth import get_refresh_view
from dj_rest_auth.registration.views import RegisterView
from dj_rest_auth.views import LoginView, LogoutView

from . import api


urlpatterns = [
    path("register/", RegisterView.as_view(), name="rest_register"),
    path("login/", LoginView.as_view(), name="rest_login"),
    path("logout/", LogoutView.as_view(), name="rest_logout"),
    path("token/refresh/", get_refresh_view().as_view(), name="rest_token_refresh"),
    path("<uuid:pk>/", api.landlord_detail, name="api-landlord-detail"),
    path(
        "my-reservations/",
        api.reservations_list,
        name="api-reservations-list",
    ),
]
