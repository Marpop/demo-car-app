from rest_framework.generics import DestroyAPIView, ListCreateAPIView

from apps.cars.models import Car
from apps.cars.serializers import CarSerializer


class CarListView(ListCreateAPIView):
    queryset = Car.objects.all()
    serializer_class = CarSerializer


class CarDestroyView(DestroyAPIView):
    queryset = Car.objects.all()
    serializer_class = CarSerializer
