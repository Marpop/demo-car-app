from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from apps.cars.models import Car


class CarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Car
        fields = (
            "id",
            "maker",
            "model",
        )
        read_only_fields = ("id",)
        validators = [
            UniqueTogetherValidator(
                queryset=Car.objects.all(),
                fields=["maker", "model"],
            )
        ]
