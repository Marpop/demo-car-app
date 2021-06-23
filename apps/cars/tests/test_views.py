from unittest.mock import ANY

from django.urls import reverse

import pytest
from rest_framework import status

from apps.cars.models import Car
from apps.cars.tests.factories import CarFactory, RateFactory

pytestmark = pytest.mark.django_db


class TestCarListView:
    @staticmethod
    def setup():
        CarFactory.create_batch(4)
        CarFactory.create(make="Volkswagen", model="Passat")

    @staticmethod
    def test_list(api_client):
        response = api_client.get(reverse("cars"))
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 5

    @staticmethod
    def test_create_ok(api_client):
        response = api_client.post(
            reverse("cars"),
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

    @staticmethod
    def test_create_exists(api_client):
        response = api_client.post(
            reverse("cars"),
            data={"make": "Volkswagen", "model": "Passat"},
            format="json",
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert Car.objects.all().count() == 5


class TestCarDestroyView:
    @staticmethod
    def setup():
        CarFactory.create_batch(4)

    @staticmethod
    def test_delete(api_client):
        car = Car.objects.first()
        response = api_client.delete(reverse("cars_detail", kwargs={"pk": car.id}))
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert Car.objects.all().count() == 3

class TestPopularCarsListView:
    @staticmethod
    def setup():
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

    @staticmethod
    def test_list(api_client):
        response = api_client.get(reverse("popular"))
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == [{"id":ANY,"make": "Mercedes","model":ANY,"rates_number":5,},{"id": ANY,"make": "BMW","model": ANY,"rates_number": 3,},{"id": ANY,"make": "Volkswagen","model": ANY,"rates_number":0}]

class TestRateCarView:
    @staticmethod
    def setup():
        CarFactory.create(id=2)

    @staticmethod
    def test_create_ok(api_client):
        response = api_client.post(
            reverse("rate"),
            data={
                "car_id": 2,
                "rating": 3,
            },
            format="json",
        )
        print(response)
        print(response.json())
        assert response.status_code == status.HTTP_201_CREATED
        assert response.json() == {
            "car_id": 2,
            "rating": 3,
        }

    @staticmethod
    def test_create_no_car(api_client):
        response = api_client.post(
            reverse("rate"),
            data={
                "car_id": 999,
                "rating": 3,
            },
            format="json",
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST
