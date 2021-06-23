import pytest
from pytest_factoryboy import register
from rest_framework.test import APIClient

from apps.cars.tests.factories import CarFactory, RateFactory

register(CarFactory)
register(RateFactory)


@pytest.fixture
def api_client():
    return APIClient()
