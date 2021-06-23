from django.db.models import Count

from rest_framework.generics import (
    DestroyAPIView,
    ListCreateAPIView,
)

from apps.cars.models import Car, Rate
from apps.cars.serializers import CarSerializer


class CarListView(ListCreateAPIView):
    queryset = Car.objects.all()
    serializer_class = CarSerializer


class CarListDestroyView(DestroyAPIView):
    queryset = Car.objects.all()
    serializer_class = CarSerializer
