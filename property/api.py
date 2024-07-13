from django.http import JsonResponse
from django.db.models import BooleanField, Case, When, Q

from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes,
)
from rest_framework_simplejwt.tokens import AccessToken

from .models import Property, Reservation
from .forms import PropertyForm
from .searilizers import (
    PropertyListSearilizer,
    PropertyDetailSearilizer,
    ReservationsListSearilizer,
)


@api_view(["GET"])
@authentication_classes([])
@permission_classes([])
def properties_list(request):
    try:
        token = request.META.get("HTTP_AUTHORIZATION").split("Bearer ")[1]
        token = AccessToken(token)
        user_id = token.payload.get("user_id")
    except Exception as e:
        user_id = None

    properties = Property.objects.all()

    landlord_id = request.GET.get("landlord_id")
    favourites_only = request.GET.get("favourites")
    country = request.GET.get("country")
    category = request.GET.get("category")
    number_of_guests = request.GET.get("numGuests")
    number_of_bedrooms = request.GET.get("numBedrooms")
    number_of_bathrooms = request.GET.get("numBathrooms")
    check_in_date = request.GET.get("checkInDate")
    check_out_date = request.GET.get("checkOutDate")

    kwargs = {}

    if landlord_id:
        kwargs["landlord_id"] = landlord_id

    if favourites_only:
        kwargs["favourited__id"] = user_id

    if country:
        kwargs["country"] = country

    if category:
        kwargs["category"] = category

    if number_of_guests:
        kwargs["guests__gte"] = number_of_guests

    if number_of_bedrooms:
        kwargs["bedrooms__gte"] = number_of_bedrooms

    if number_of_bathrooms:
        kwargs["bathrooms__gte"] = number_of_bathrooms

    if check_in_date and check_out_date:
        properties = properties.filter(
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

    properties = properties.filter(**kwargs)

    if user_id:
        properties = properties.annotate(
            is_favourite=Case(
                When(favourited__id=user_id, then=True),
                default=False,
                output_field=BooleanField(),
            )
        )

    searilizer = PropertyListSearilizer(properties, many=True)
    return JsonResponse({"data": searilizer.data})


@api_view(["POST", "FILES"])
def create_property(request):
    form = PropertyForm(request.POST, request.FILES)

    if form.is_valid():
        property = form.save(commit=False)
        property.landlord = request.user
        property.save()

        return JsonResponse({"success": True})
    else:
        print("error", form.errors, form.non_field_errors)
        return JsonResponse({"error": form.errors.as_json()}, status=400)


@api_view(["GET"])
@authentication_classes([])
@permission_classes([])
def property_detail(request, pk):
    property = Property.objects.get(pk=pk)
    searilizer = PropertyDetailSearilizer(property, many=False)
    return JsonResponse(searilizer.data)


@api_view(["POST"])
def book_property(request, pk):
    try:
        start_date = request.POST.get("start_date", "")
        end_date = request.POST.get("end_date", "")
        number_of_nights = request.POST.get("number_of_nights", "")
        guests = request.POST.get("guests", "")
        total_price = request.POST.get("total_price", "")

        property = Property.objects.get(pk=pk)

        Reservation.objects.create(
            property=property,
            start_date=start_date,
            end_date=end_date,
            number_of_nights=number_of_nights,
            guests=guests,
            total_price=total_price,
            created_by=request.user,
        )
        return JsonResponse({"success": True})
    except Exception as e:
        print("Error", e)
        return JsonResponse({"success": False})


@api_view(["GET"])
@authentication_classes([])
@permission_classes([])
def property_reservations(request, pk):
    reservations = Reservation.objects.filter(property__id=pk)
    searilizer = ReservationsListSearilizer(reservations, many=True)
    return JsonResponse(searilizer.data, safe=False)


@api_view(["POST"])
def toggle_favourite(request, pk):
    property = Property.objects.get(pk=pk)

    if request.user in property.favourited.all():
        property.favourited.remove(request.user)
        is_favourite = False
    else:
        property.favourited.add(request.user)
        is_favourite = True
    return JsonResponse({"is_favourite": is_favourite})
