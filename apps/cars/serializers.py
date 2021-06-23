from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from apps.cars.models import Car, Rate


class CarSerializer(serializers.ModelSerializer):

    avg_rating = serializers.Field(required=False)

    class Meta:
        model = Car
        fields = (
            "id",
            "maker",
            "model",
            "avg_rating",
        )
        read_only_fields = ("id", "avg_rating")
        validators = [
            UniqueTogetherValidator(
                queryset=Car.objects.all(),
                fields=["maker", "model"],
            )
        ]


class RateCarSerializer(serializers.ModelSerializer):

    car_id = serializers.PrimaryKeyRelatedField(
        source="car", queryset=Car.objects.all()
    )

    class Meta:
        model = Rate
        fields = ("car_id", "rating")
