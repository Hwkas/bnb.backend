from rest_framework import serializers

from app.models import Property
from app.searilizers.user import UserDetailSearilizer


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
