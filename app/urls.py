from django.urls import path

from app.apis import conversation, property, reservation, user


user_urls = [
    path(
        "user/",
        user.register,
        name="api-user-register",
    ),
    path(
        "user/<int:id>/",
        user.get,
        name="api-landlord-detail",
    ),
    path(
        "user/login/",
        user.login,
        name="api-user-login",
    ),
    path(
        "user/token-refresh/",
        user.token_refresh,
        name="api-user-token-refresh",
    ),
]

property_urls = [
    path(
        "property/",
        property.list,
        name="api-properties-list",
    ),
    path(
        "property/create/",
        property.create,
        name="api-create-property",
    ),
    path(
        "property/<int:id>/",
        property.retrieve,
        name="api-property-detail",
    ),
    path(
        "property/<int:id>/toggle-favourite/",
        property.toggle_favourite,
        name="api-property-toggle-favourite ",
    ),
]

reservation_urls = [
    path(
        "reservation/",
        reservation.list,
        name="api-reservations-list",
    ),
    path(
        "reservation/<int:property_id>/book/",
        reservation.create,
        name="api-book-reservation",
    ),
]

conversation_url = [
    path("conversation/", conversation.list, name="api-conversations-list"),
    path(
        "conversation/<int:id>/", conversation.detail, name="api-conversations-detail"
    ),
    path(
        "conversation/start/<int:user_id>/",
        conversation.start,
        name="api-conversations-start",
    ),
]

urlpatterns = user_urls + property_urls + reservation_urls + conversation_url
