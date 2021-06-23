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

    @staticmethod
    def test_avg_rating_none():
        car = CarFactory.create(maker="Volkswagen", model="Golf")
        assert car.avg_rating is None

    @staticmethod
    def test_avg_rating_one():
        car = CarFactory.create(maker="Volkswagen", model="Golf")
        RateFactory(car=car, rating=2)
        assert car.avg_rating == 2

    @staticmethod
    def test_avg_rating_average():
        car = CarFactory.create(maker="Volkswagen", model="Golf")
        RateFactory(car=car, rating=2)
        RateFactory(car=car, rating=2)
        RateFactory(car=car, rating=3)
        RateFactory(car=car, rating=4)
        assert car.avg_rating == 2.8


class TestRate:
    @staticmethod
    def test_factory(rate):
        assert Rate.objects.count() == 1
        assert rate == Rate.objects.first()

    @staticmethod
    def test_str():
        car = CarFactory.create(maker="Volkswagen", model="Golf")
        rate = RateFactory.create(car=car, rating=3)
        assert str(rate) == "Volkswagen Golf: 3"
