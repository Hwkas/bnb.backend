from contextlib import suppress
from datetime import datetime

from rest_framework.exceptions import ValidationError

from oauth2_provider.models import AccessToken, Application, RefreshToken
from oauthlib.common import generate_token


def get_access_token(*, token: str) -> AccessToken:
    with suppress(AccessToken.DoesNotExist):
        return AccessToken.objects.get(token=token)
    raise ValidationError(
        detail={"error": "access_token doesn't exists."}, code="access_token"
    )


def get_refresh_token(*, token: str, revoked__isnull: bool = None) -> RefreshToken:
    with suppress(RefreshToken.DoesNotExist):
        kwargs = {"token": token}
        if revoked__isnull:
            kwargs.update(revoked__isnull=revoked__isnull)
        return RefreshToken.objects.get(**kwargs)
    raise ValidationError(
        detail={"error": "refresh_token doesn't exists."}, code="refresh_token"
    )


def get_application(*, client_id: str, authorization_grant_type: str) -> Application:
    with suppress(Application.DoesNotExist):
        return Application.objects.get(
            client_id=client_id, authorization_grant_type=authorization_grant_type
        )
    raise ValidationError(
        detail={"error": "application doesn't exists."}, code="application"
    )


def create_access_token(
    *, application_id: int, user_id: int, expires: datetime
) -> AccessToken:
    return AccessToken.objects.create(
        application_id=application_id,
        user_id=user_id,
        token=generate_token(),
        expires=expires,
    )


def create_refresh_token(
    *, application_id: int, user_id: int, access_token_id: int
) -> RefreshToken:
    return RefreshToken.objects.create(
        application_id=application_id,
        user_id=user_id,
        access_token_id=access_token_id,
        token=generate_token(),
    )
