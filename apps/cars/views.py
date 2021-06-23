from django.db import models

from rest_framework.generics import (
    CreateAPIView,
    DestroyAPIView,
    ListAPIView,
    ListCreateAPIView,
)

from apps.cars.models import Car, Rate
from apps.cars.serializers import (
    CarSerializer,
    PopularCarSerializer,
    RateCarSerializer,
)


class CarListView(ListCreateAPIView):
    queryset = Car.objects.all()
    serializer_class = CarSerializer


class CarDestroyView(DestroyAPIView):
    queryset = Car.objects.all()
    serializer_class = CarSerializer


class PopularCarsListView(ListAPIView):
    queryset = Car.objects.annotate(rates_number=models.Count("rates")).order_by(
        "-rates_number"
    )
    serializer_class = PopularCarSerializer


class RateCarView(CreateAPIView):
    queryset = Rate.objects.all()
    serializer_class = RateCarSerializer
