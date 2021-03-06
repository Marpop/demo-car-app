import factory

from apps.cars.models import Car, Rate


class CarFactory(factory.django.DjangoModelFactory):
    make = factory.Faker("word")
    model = factory.Faker("word")

    class Meta:
        model = Car


class RateFactory(factory.django.DjangoModelFactory):
    rating = factory.Faker("pyint", min_value=1, max_value=5)
    car = factory.SubFactory(CarFactory)

    class Meta:
        model = Rate
