from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from apps.cars.models import Car


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
