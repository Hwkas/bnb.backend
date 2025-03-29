from contextlib import suppress
from typing import List, Union

from rest_framework.exceptions import ValidationError

from app.models import User


def create(
    *,
    username: str,
    password: str,
    first_name: str = None,
    last_name: str = None,
    email: str = None,
) -> User:
    kwargs = {}

    if first_name:
        kwargs.update(first_name=first_name)
    if last_name:
        kwargs.update(last_name=last_name)
    if email:
        kwargs.update(email=email)

    user, create = User.objects.get_or_create(username=username, defaults=kwargs)

    if not create:
        raise ValidationError(
            detail={"error": "username already exists."}, code="username"
        )
    user.set_password(password)
    user.save()
    return user


def filter(*, username: str, check_existance: bool = False) -> Union[List[User], bool]:
    kwargs = {"username": username}

    query = User.objects.filter(**kwargs)

    if check_existance:
        query = query.exists()
    return query


def get(*, username: str = None, id: int = None):
    kwargs = {}

    if username:
        kwargs.update(username=username)
    if id:
        kwargs.update(id=id)
    with suppress(User.DoesNotExist):
        return User.objects.get(**kwargs)
    raise ValidationError(detail={"error": "user doesn't exists."}, code="user")
