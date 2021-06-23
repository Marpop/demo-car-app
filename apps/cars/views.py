from rest_framework.generics import (
    CreateAPIView,
    DestroyAPIView,
    ListAPIView,
    ListCreateAPIView,
)

from apps.cars.models import Car, Rate
from apps.cars.serializers import CarSerializer, RateCarSerializer


class CarListView(ListCreateAPIView):
    queryset = Car.objects.all()
    serializer_class = CarSerializer


class CarDestroyView(DestroyAPIView):
    queryset = Car.objects.all()
    serializer_class = CarSerializer

class RateCarView(CreateAPIView):
    queryset = Rate.objects.all()
    serializer_class = RateCarSerializer
