from channels.db import database_sync_to_async
from channels.middleware import BaseMiddleware

from django.contrib.auth.models import AnonymousUser

from app.models import User
from app.queries import (
    oauth as oauth_queries,
    user as user_queries,
)


@database_sync_to_async
def get_user(token_key) -> User:
    try:
        token = oauth_queries.get_access_token(token=token_key)
        return user_queries.get(id=token.user_id)
    except Exception:
        return AnonymousUser


class TokenAuthMiddleware(BaseMiddleware):
    def __init__(self, inner):
        self.inner = inner

    async def __call__(self, scope, receive, send):
        query = dict(
            x.split("=") for x in scope.get("query_string").decode().split("&")
        )

        token_key = query.get("token")

        scope["user"] = await get_user(token_key)
        return await super().__call__(scope, receive, send)
