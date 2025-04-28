from rest_framework import serializers

from app.models import Reservation
from app.searilizers.property import PropertyListSearilizer


class ReservationsListSearilizer(serializers.ModelSerializer):
    property = PropertyListSearilizer(read_only=True, many=False)

    class Meta:
        model = Reservation
        fields = (
            "id",
            "start_date",
            "end_date",
            "number_of_nights",
            "total_price",
            "property",
        )
