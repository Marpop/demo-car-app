from django.urls import reverse
from unittest.mock import ANY

import pytest
from rest_framework import status

from apps.cars.models import Car
from apps.cars.tests.factories import CarFactory

pytestmark = pytest.mark.django_db


class TestCarListView:
    def setup(self):
        CarFactory.create_batch(4)
        CarFactory.create(maker="Volkswagen", model="Passat")

    def test_list(self, api_client):
        response = api_client.get(reverse("cars"))
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 5

    def test_create_ok(self, api_client):
        response = api_client.post(
            reverse("cars"),
            data={"maker": "Volkswagen", "model": "Golf"},
            format="json",
        )
        assert response.status_code == status.HTTP_201_CREATED
        assert response.json() == {"id": ANY, "maker": "Volkswagen", "model": "Golf", "avg_rating": None}
        assert Car.objects.all().count() == 6


    def test_create_exists(self, api_client):
        response = api_client.post(
            reverse("cars"),
            data={"maker": "Volkswagen", "model": "Passat"},
            format="json"
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert Car.objects.all().count() == 5

class TestCarDestroyView:

    def setup(self):
        CarFactory.create_batch(4)

    def test_delete(self, api_client):
        car = Car.objects.first()
        response = api_client.delete(reverse("cars_detail", kwargs={'pk': car.id}))
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert Car.objects.all().count() == 3
