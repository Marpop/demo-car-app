import pytest

from apps.cars.models import Car, Rate
from apps.cars.tests.factories import CarFactory, RateFactory

pytestmark = pytest.mark.django_db


class TestCar:
    @staticmethod
    def test_factory(car):
        assert Car.objects.count() == 1
        assert car == Car.objects.first()

    @staticmethod
    def test_str():
        car = CarFactory.create(maker="Volkswagen", model="Golf")
        assert str(car) == "Volkswagen Golf"


class TestRate:
    @staticmethod
    def test_factory(rate):
        assert Rate.objects.count() == 1
        assert rate == Rate.objects.first()

    @staticmethod
    def test_str():
        car = CarFactory.create(maker="Volkswagen", model="Golf")
        rate = RateFactory.create(car=car, rate=3)
        assert str(rate) == "Volkswagen Golf: 3"
