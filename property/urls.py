from django.urls import path

from . import api


urlpatterns = [
    path("", api.properties_list, name="api-properties-list"),
    path("create/", api.create_property, name="api-create-property"),
    path("<uuid:pk>/", api.property_detail, name="api-property-detail"),
    path("<uuid:pk>/book/", api.book_property, name="api-book-property"),
    path(
        "<uuid:pk>/reservations/",
        api.property_reservations,
        name="api-property-reservations",
    ),
    path(
        "<uuid:pk>/toggle-favourite/",
        api.toggle_favourite,
        name="api-property-toggle-favourite ",
    ),
]
