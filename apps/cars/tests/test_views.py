from unittest.mock import ANY

from django.urls import reverse

import pytest
from rest_framework import status

from apps.cars.models import Car
from apps.cars.tests.factories import CarFactory, RateFactory

pytestmark = pytest.mark.django_db


class TestCarListView:
    def setup(self):
        CarFactory.create_batch(4)
        CarFactory.create(make="Volkswagen", model="Passat")
        self.endpoint = reverse("cars")

    def test_list(self, api_client):
        response = api_client.get(self.endpoint)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 5

    def test_create_ok(self, api_client):
        response = api_client.post(
            self.endpoint,
            data={"make": "Volkswagen", "model": "Golf"},
            format="json",
        )
        assert response.status_code == status.HTTP_201_CREATED
        assert response.json() == {
            "id": ANY,
            "make": "Volkswagen",
            "model": "Golf",
            "avg_rating": None,
        }
        assert Car.objects.all().count() == 6

    def test_create_exists(self, api_client):
        response = api_client.post(
            self.endpoint,
            data={"make": "Volkswagen", "model": "Passat"},
            format="json",
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert Car.objects.all().count() == 5


class TestCarDestroyView:
    def setup(self):
        CarFactory.create_batch(4)
        car = Car.objects.first()
        self.endpoint = reverse("cars_detail", kwargs={"pk": car.id})

    def test_delete(self, api_client):
        response = api_client.delete(self.endpoint)
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert Car.objects.all().count() == 3


class TestPopularCarsListView:
    def setup(self):
        self.endpoint = reverse("popular")
        car_1 = CarFactory.create(make="BMW")
        car_2 = CarFactory.create(make="Mercedes")
        CarFactory.create(make="Volkswagen")
        RateFactory(car=car_1)
        RateFactory(car=car_1)
        RateFactory(car=car_1)
        RateFactory(car=car_2)
        RateFactory(car=car_2)
        RateFactory(car=car_2)
        RateFactory(car=car_2)
        RateFactory(car=car_2)

    def test_list(self, api_client):
        response = api_client.get(self.endpoint)
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == [
            {
                "id": ANY,
                "make": "Mercedes",
                "model": ANY,
                "rates_number": 5,
            },
            {
                "id": ANY,
                "make": "BMW",
                "model": ANY,
                "rates_number": 3,
            },
            {"id": ANY, "make": "Volkswagen", "model": ANY, "rates_number": 0},
        ]


class TestRateCarView:
    def setup(self):
        self.endpoint = reverse("rate")

    def test_create_ok(self, api_client):
        car = CarFactory.create(id=2)
        car.refresh_from_db()
        response = api_client.post(
            self.endpoint,
            data={
                "car_id": 2,
                "rating": 3,
            },
            format="json",
        )
        assert response.status_code == status.HTTP_201_CREATED
        assert response.json() == {
            "car_id": 2,
            "rating": 3,
        }

    def test_create_no_car(self, api_client):
        response = api_client.post(
            self.endpoint,
            data={
                "car_id": 1,
                "rating": 3,
            },
            format="json",
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST
