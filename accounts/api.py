from django.http import JsonResponse

from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes,
)

from property.searilizers import ReservationsListSearilizer

from .models import User
from .searilizers import UserDetailSearilizer


@api_view(["GET"])
@authentication_classes([])
@permission_classes([])
def landlord_detail(request, pk: int) -> JsonResponse:
    user = User.objects.get(pk=pk)
    searilizer = UserDetailSearilizer(user, many=False)
    return JsonResponse(searilizer.data, safe=False)


@api_view(["GET"])
def reservations_list(request) -> JsonResponse:
    reservations = request.user.reservations.all()
    searilizer = ReservationsListSearilizer(reservations, many=True)
    return JsonResponse(searilizer.data, safe=False)
