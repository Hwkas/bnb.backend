from datetime import timedelta
from typing import Dict

from django.conf import settings
from django.utils import timezone

from rest_framework.exceptions import ValidationError

from app.models import User
from app.queries import (
    oauth as oauth_queries,
    user as user_queries,
)


def generate_access_token_response(
    *,
    client_id: str,
    grant_type: str,
    user: User = None,
    username: str = None,
    password: str = None,
) -> Dict:
    if not user:
        user = user_queries.get(username=username)

        if not user.check_password(password):
            raise ValidationError(
                detail={"error": "invalid password."}, code="password"
            )

    application = oauth_queries.get_application(
        client_id=client_id, authorization_grant_type=grant_type
    )

    user.last_login = timezone.now()
    user.save()

    access_token_expire_seconds = settings.OAUTH2_PROVIDER.get(
        "ACCESS_TOKEN_EXPIRE_SECONDS"
    )

    access_token = oauth_queries.create_access_token(
        application_id=application.id,
        user_id=user.id,
        expires=timezone.now() + timedelta(seconds=access_token_expire_seconds),
    )

    refresh_token = oauth_queries.create_refresh_token(
        application_id=application.id,
        user_id=user.id,
        access_token_id=access_token.id,
    )

    return {
        "user_id": user.id,
        "access_token": access_token.token,
        "expires_in": access_token_expire_seconds,
        "token_type": "Bearer",
        "scope": "read write",
        "refresh_token": refresh_token.token,
    }


def generate_token_refresh_response(
    *, client_id: str, grant_type: str, refresh_token: str
) -> Dict:
    refresh_token = oauth_queries.get_refresh_token(
        token=refresh_token, revoked__isnull=True
    )
    refresh_token.revoke()
    refresh_token_expire_seconds = settings.OAUTH2_PROVIDER.get(
        "REFRESH_TOKEN_EXPIRE_SECONDS"
    )
    if (
        refresh_token.user.last_login + timedelta(seconds=refresh_token_expire_seconds)
        <= timezone.now()
    ):
        raise ValidationError(
            detail={"error": "refresh_token expired."}, code="refresh_token"
        )

    application = oauth_queries.get_application(
        client_id=client_id, authorization_grant_type=grant_type
    )

    access_token_expire_seconds = settings.OAUTH2_PROVIDER.get(
        "ACCESS_TOKEN_EXPIRE_SECONDS"
    )

    access_token = oauth_queries.create_access_token(
        application_id=application.id,
        user_id=refresh_token.user_id,
        expires=timezone.now() + timedelta(seconds=access_token_expire_seconds),
    )

    refresh_token = oauth_queries.create_refresh_token(
        application_id=application.id,
        user_id=refresh_token.user_id,
        access_token_id=access_token.id,
    )

    return {
        "user_id": refresh_token.user_id,
        "access_token": access_token.token,
        "expires_in": access_token_expire_seconds,
        "token_type": "Bearer",
        "scope": "read write",
        "refresh_token": refresh_token.token,
    }
