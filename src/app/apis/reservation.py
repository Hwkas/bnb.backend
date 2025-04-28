from datetime import date

from django.http import JsonResponse

from rest_framework import status
from rest_framework.decorators import (
    api_view,
    permission_classes,
)
from rest_framework.exceptions import ValidationError

from dateutil.parser import parse

from app import constants
from app.queries import (
    property as property_queries,
    reservation as reservation_queries,
)
from app.searilizers import ReservationsListSearilizer


@api_view(["GET"])
@permission_classes([])
def list(request) -> JsonResponse:
    user_reservations = request.GET.get("user_reservations").lower() == "true"
    reservations = reservation_queries.filter(
        patron_id=request.user.id if user_reservations else None,
        property_id=request.GET.get("property_id"),
    )
    searilizer = ReservationsListSearilizer(reservations, many=True)
    return JsonResponse(data={"results": searilizer.data})


@api_view(["POST"])
def create(request, property_id: int) -> JsonResponse:
    user_id = request.user.id
    start_date = request.data.get("start_date")
    end_date = request.data.get("end_date")
    number_of_nights = int(request.data.get("number_of_nights"))
    guests = int(request.data.get("guests"))

    if not property_id:
        raise ValidationError(
            detail={"error": "property_id is a required param."}, code="property_id"
        )
    if not start_date or not end_date:
        raise ValidationError(
            detail={"error": "start_date & end_date is a required param."},
            code="dates",
        )
    if parse(start_date).date() < date.today() or parse(end_date).date() < date.today():
        raise ValidationError(
            detail={"error": "invalid start_date or end_date."},
            code="dates",
        )
    if not number_of_nights:
        raise ValidationError(
            detail={"error": "number_of_nights is a required param."},
            code="number_of_nights",
        )
    if not guests:
        raise ValidationError(
            detail={"error": "guests is a required param."}, code="guests"
        )

    if reservation_queries.filter(
        property_id=property_id,
        start_date=start_date,
        end_date=end_date,
        check_existance=True,
    ):
        raise ValidationError(
            detail={"error": "reservation for these dates already exists."},
            code="reservation",
        )

    property = property_queries.get(id=property_id)

    total_price = (
        property.price_per_night + constants.PLATFORM_FEE_PER_NIGHT
    ) * number_of_nights

    reservation_queries.create(
        property_id=property_id,
        start_date=start_date,
        end_date=end_date,
        number_of_nights=number_of_nights,
        guests=guests,
        total_price=total_price,
        patron_id=user_id,
    )
    return JsonResponse(data={"success": True}, status=status.HTTP_201_CREATED)
