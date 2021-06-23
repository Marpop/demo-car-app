from django.urls import reverse

import pytest
from rest_framework import status

from apps.cars.models import Car
from apps.cars.tests.factories import CarFactory

pytestmark = pytest.mark.django_db


class TestCarListView:
    def setup(self):
        CarFactory.create_batch(5)

    def test_category_recommended(self, api_client):
        response = api_client.get(reverse("cars"))
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 5


class TestCarDestroylView(TestCarListView):
    def test_delete(self, api_client):
        car = Car.objects.first()
        response = api_client.post(reverse("cars-detail", args=[car.id]))
        assert response.status_code == status.HTTP_200_OK
