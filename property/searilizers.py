from rest_framework import serializers

from accounts.searilizers import UserDetailSearilizer

from .models import Property, Reservation


class PropertyListSearilizer(serializers.ModelSerializer):
    is_favourite = serializers.SerializerMethodField()

    def get_is_favourite(self, obj):
        return obj.is_favourite if hasattr(obj, "is_favourite") else None

    class Meta:
        model = Property
        fields = (
            "id",
            "title",
            "price_per_night",
            "image_url",
            "is_favourite",
        )


class PropertyDetailSearilizer(serializers.ModelSerializer):
    landlord = UserDetailSearilizer(read_only=True, many=False)

    class Meta:
        model = Property
        fields = (
            "id",
            "title",
            "price_per_night",
            "image_url",
            "bedrooms",
            "bathrooms",
            "guests",
            "description",
            "landlord",
        )


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
