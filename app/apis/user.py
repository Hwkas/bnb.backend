from django.http import JsonResponse

from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes,
)
from rest_framework.exceptions import ValidationError

from app.queries import user as user_queries
from app.searilizers import UserDetailSearilizer
from app.tasks import oauth as oauth_tasks


@api_view(["POST"])
@authentication_classes([])
@permission_classes([])
def register(request) -> JsonResponse:
    client_id = request.headers.get("Client-Id")
    grant_type = request.data.get("grant_type")
    username = request.data.get("username")
    password1 = request.data.get("password1")
    password2 = request.data.get("password2")

    if not client_id:
        raise ValidationError(
            detail={"client_id": "client_id is a required param."}, code="client_id"
        )

    if not grant_type:
        raise ValidationError(
            detail={"error": "grant_type is a required param."}, code="grant_type"
        )

    if not username:
        raise ValidationError(
            detail={"error": "username is a required param."}, code="username"
        )

    if not password1 or not password2:
        raise ValidationError(
            detail={"error": "password is a required param."}, code="password"
        )

    if password1 != password2:
        raise ValidationError(
            detail={"error": "password is a not matching."}, code="password"
        )

    user = user_queries.create(
        username=username,
        password=password1,
    )

    respone = oauth_tasks.generate_access_token_response(
        client_id=client_id, grant_type=grant_type, user=user
    )
    return JsonResponse(respone, safe=False)


@api_view(["GET"])
@authentication_classes([])
@permission_classes([])
def get(request, id: int) -> JsonResponse:
    searilizer = UserDetailSearilizer(user_queries.get(id=id), many=False)
    return JsonResponse(searilizer.data, safe=False)


@api_view(["POST"])
@authentication_classes([])
@permission_classes([])
def login(request) -> JsonResponse:
    client_id = request.headers.get("Client-Id")
    grant_type = request.data.get("grant_type")
    username = request.data.get("username")
    password = request.data.get("password")

    if not client_id:
        raise ValidationError(
            detail={"client_id": "client_id is a required param."}, code="client_id"
        )

    if not grant_type:
        raise ValidationError(
            detail={"error": "grant_type is a required param."}, code="grant_type"
        )

    if not username:
        raise ValidationError(
            detail={"error": "username is a required param."},
            code="username",
        )

    if not password:
        raise ValidationError(
            detail={"error": "password is a required param."}, code="password"
        )

    respone = oauth_tasks.generate_access_token_response(
        client_id=client_id, grant_type=grant_type, username=username, password=password
    )
    return JsonResponse(respone, safe=False)


@api_view(["POST"])
@authentication_classes([])
@permission_classes([])
def token_refresh(request) -> JsonResponse:
    client_id = request.headers.get("Client-Id")
    grant_type = request.data.get("grant_type")
    refresh_token = request.data.get("refresh_token")

    if not client_id:
        raise ValidationError(
            detail={"client_id": "client_id is a required param."}, code="client_id"
        )

    if not refresh_token:
        raise ValidationError(
            detail={"error": "refresh_token is a required param."}, code="refresh_token"
        )

    respone = oauth_tasks.generate_token_refresh_response(
        client_id=client_id, grant_type=grant_type, refresh_token=refresh_token
    )
    return JsonResponse(respone, safe=False)
