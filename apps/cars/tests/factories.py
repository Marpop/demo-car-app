import factory
from content.models import Car, Rate


class CarFactory(factory.django.DjangoModelFactory):
    maker = factory.Faker("word")
    model = factory.Faker("word")

    class Meta:
        model = Car


class RateFactory(factory.django.DjangoModelFactory):
    rate = factory.Faker("pyint", min_value=1, max_value=5)
    car = factory.SubFactory(CarFactory)

    class Meta:
        model = Rate
