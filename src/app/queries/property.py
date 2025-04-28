from contextlib import suppress
from typing import List

from django.db.models import Count, Q

from rest_framework.exceptions import ValidationError

from app.models import Property, User


def create(
    *,
    title: str,
    description: str,
    price_per_night: int,
    bedrooms: int,
    bathrooms: int,
    guests: int,
    country: str,
    country_code: str,
    category: str,
    image: str,
) -> Property:
    kwargs = {
        "title": title,
        "description": description,
        "price_per_night": price_per_night,
        "bedrooms": bedrooms,
        "bathrooms": bathrooms,
        "guests": guests,
        "country": country,
        "country_code": country_code,
        "category": category,
        "image": image,
    }
    return Property.objects.create(**kwargs)


def filter(
    *,
    user_id: int = None,
    price_per_night: int = None,
    bedrooms: int = None,
    bathrooms: int = None,
    guests: int = None,
    country: str = None,
    category: str = None,
    landlord_id: int = None,
    favourited: bool = None,
    check_in_date: str = None,
    check_out_date: str = None,
) -> List[Property]:
    kwargs = {}

    if price_per_night:
        kwargs.update(price_per_night__lte=price_per_night)
    if bedrooms:
        kwargs.update(bedrooms__gte=bedrooms)
    if bathrooms:
        kwargs.update(bathrooms__gte=bathrooms)
    if guests:
        kwargs.update(guests__gte=guests)
    if country:
        kwargs.update(country=country)
    if category:
        kwargs.update(category=category)
    if landlord_id:
        kwargs.update(landlord_id=landlord_id)
    if favourited is True and user_id:
        kwargs.update(favourited__id=user_id)

    query = Property.objects.filter(**kwargs)

    if favourited is False:
        query = query.filter(~Q(favourited__id=user_id))

    if check_in_date and check_out_date:
        query = query.filter(
            ~Q(
                (
                    Q(reservations__start_date__lte=check_in_date)
                    & Q(reservations__end_date__gte=check_in_date)
                )
                | (
                    Q(reservations__start_date__lte=check_out_date)
                    & Q(reservations__end_date__gte=check_out_date)
                )
                | (
                    Q(reservations__start_date__gte=check_in_date)
                    & Q(reservations__start_date__lte=check_out_date)
                )
                | (
                    Q(reservations__end_date__gte=check_in_date)
                    & Q(reservations__end_date__lte=check_out_date)
                )
            )
        )

    if user_id:
        query = query.annotate(
            is_favourite=Count("favourited", filter=Q(favourited__id=user_id))
        )
    return query


def get(*, id: int) -> Property:
    with suppress(Property.DoesNotExist):
        return Property.objects.get(id=id)
    raise ValidationError(detail={"error": "property doesn't exists."}, code="property")


def toggle_favourite(*, id: int, user: User) -> bool:
    query = Property.objects.get(id=id)

    if is_favourite := not query.favourited.filter(id=user.id).exists():
        query.favourited.add(user)
    else:
        query.favourited.remove(user)
    return is_favourite
