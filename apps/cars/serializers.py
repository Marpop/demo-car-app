from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from apps.cars.models import Car, Rate
from apps.cars.services import get_models_for_make


class CarSerializer(serializers.ModelSerializer):

    avg_rating = serializers.ReadOnlyField()

    class Meta:
        model = Car
        fields = (
            "id",
            "make",
            "model",
            "avg_rating",
        )
        read_only_fields = ("id", "avg_rating")
        validators = [
            UniqueTogetherValidator(
                queryset=Car.objects.all(),
                fields=["make", "model"],
            )
        ]

    def validate(self, data):
        make = data["make"].capitalize()
        model = data["model"].capitalize()
        results = get_models_for_make(make)
        if len(results) == 0:
            raise serializers.ValidationError({"make": f"Make '{make}' does't exist."})
        make_found = False
        for result in results:
            if result["Model_Name"].lower() == model.lower():
                make_found = True
        if not make_found:
            raise serializers.ValidationError(
                {"model": f"Model '{model}' does't exist."}
            )
        return {"make": make, "model": model}


class PopularCarSerializer(serializers.ModelSerializer):

    rates_number = serializers.SerializerMethodField()

    class Meta:
        model = Car
        fields = (
            "id",
            "make",
            "model",
            "rates_number",
        )

    @staticmethod
    def get_rates_number(obj):
        return obj.rates.count()


class RateCarSerializer(serializers.ModelSerializer):

    car_id = serializers.PrimaryKeyRelatedField(
        source="car", queryset=Car.objects.all()
    )

    class Meta:
        model = Rate
        fields = ("car_id", "rating")
