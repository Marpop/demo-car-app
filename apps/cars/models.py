from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models import Avg

from model_utils.models import TimeStampedModel


class Car(TimeStampedModel):
    maker = models.CharField(max_length=50)
    model = models.CharField(max_length=50)

    class Meta:
        constraints = [
            models.UniqueConstraint(name="unique name", fields=["maker", "model"])
        ]

    def __str__(self):
        return f"{self.maker} {self.model}"

    @property
    def avg_rating(self):
        return self.rates.all().aggregate(Avg("rate")).get("rate__avg")


class Rate(TimeStampedModel):
    car = models.ForeignKey(Car, related_name="rates", on_delete=models.CASCADE)
    rate = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )

    def __str__(self):
        return f"{self.car}: {self.rate}"
