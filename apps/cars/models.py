from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models import Avg

from model_utils.models import TimeStampedModel


class Car(TimeStampedModel):
    make = models.CharField(max_length=50)
    model = models.CharField(max_length=50)

    class Meta:
        constraints = [
            models.UniqueConstraint(name="unique name", fields=["make", "model"])
        ]

    def __str__(self):
        return f"{self.make} {self.model}"

    @property
    def avg_rating(self):
        if not self.rates.exists():
            return None
        return round(self.rates.all().aggregate(Avg("rating")).get("rating__avg"), 1)


class Rate(TimeStampedModel):
    car = models.ForeignKey(Car, related_name="rates", on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )

    def __str__(self):
        return f"{self.car}: {self.rating}"
