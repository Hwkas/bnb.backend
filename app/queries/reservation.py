from typing import List, Union

from django.db.models import Q

from app.models import Reservation


def filter(
    *,
    patron_id: int = None,
    property_id: int = None,
    start_date: str = None,
    end_date: str = None,
    check_existance: bool = None,
) -> Union[List[Reservation] | bool]:
    kwargs = {}
    if patron_id:
        kwargs.update(patron_id=patron_id)
    if property_id:
        kwargs.update(property_id=property_id)

    query = Reservation.objects.filter(**kwargs)

    if start_date and end_date:
        query = query.filter(
            (Q(start_date__lte=start_date) & Q(end_date__gte=start_date))
            | (Q(start_date__lte=end_date) & Q(end_date__gte=end_date))
            | (Q(start_date__gte=start_date) & Q(start_date__lte=end_date))
            | (Q(end_date__gte=start_date) & Q(end_date__lte=end_date))
        )

    if check_existance:
        query = query.exists()
    return query


def create(
    *,
    property_id: int,
    start_date: str,
    end_date: str,
    number_of_nights: int,
    guests: int,
    total_price: int,
    patron_id: int,
) -> Reservation:
    kwargs = {
        "property_id": property_id,
        "start_date": start_date,
        "end_date": end_date,
        "number_of_nights": number_of_nights,
        "guests": guests,
        "total_price": total_price,
        "patron_id": patron_id,
    }
    return Reservation.objects.create(**kwargs)
