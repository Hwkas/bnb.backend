from django.http import JsonResponse

from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes,
)

from app.forms import PropertyForm
from app.queries import property as property_queries
from app.searilizers import PropertyDetailSearilizer, PropertyListSearilizer


@api_view(["GET"])
@permission_classes([])
def list(request) -> JsonResponse:
    properties = property_queries.filter(
        user_id=request.user.id,
        bedrooms=request.GET.get("numBedrooms"),
        bathrooms=request.GET.get("numBathrooms"),
        guests=request.GET.get("numGuests"),
        country=request.GET.get("country"),
        category=request.GET.get("category"),
        landlord_id=request.GET.get("landlord_id"),
        favourited=request.GET.get("favourited"),
        check_in_date=request.GET.get("checkInDate"),
        check_out_date=request.GET.get("checkOutDate"),
    )

    searilizer = PropertyListSearilizer(properties, many=True)
    return JsonResponse({"data": searilizer.data})


@api_view(["POST", "FILES"])
def create(request) -> JsonResponse:
    form = PropertyForm(request.POST, request.FILES)

    if form.is_valid():
        property = form.save(commit=False)
        property.landlord = request.user
        property.save()
        return JsonResponse({"success": True})
    else:
        return JsonResponse({"error": form.errors.as_json()}, status=400)


@api_view(["GET"])
@authentication_classes([])
@permission_classes([])
def retrieve(request, id: int) -> JsonResponse:
    searilizer = PropertyDetailSearilizer(property_queries.get(id=id), many=False)
    return JsonResponse(searilizer.data)


@api_view(["POST"])
def toggle_favourite(request, id: int) -> JsonResponse:
    return JsonResponse(
        {"is_favourite": property_queries.toggle_favourite(id=id, user=request.user)}
    )
