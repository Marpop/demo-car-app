import pytest
from pytest_factoryboy import register

from content.tests.factories import CarFactory, RateFactory
from rest_framework.test import APIClient

register(CarFactory)
register(RateFactory)

@pytest.fixture
def api_client():
    return APIClient()
