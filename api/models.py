from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models


class User(AbstractUser):
    def __str__(self):
        return f"{self.username} ({self.email})"


class Station(models.Model):
    name = models.CharField(max_length=63)
    latitude = models.FloatField()
    longitude = models.FloatField()

    def __str__(self):
        return self.name


class Route(models.Model):
    source = models.ForeignKey(Station, related_name="departing_routes",
                               on_delete=models.CASCADE)
    destination = models.ForeignKey(Station, related_name="arriving_routes",
                                    on_delete=models.CASCADE)
    distance = models.PositiveIntegerField()

    def clean(self):
        if self.source == self.destination:
            raise ValidationError(
                "Source and destination stations cannot be the same.")

    def __str__(self):
        return f"{self.source.name} - {self.destination.name}"


class TrainType(models.Model):
    name = models.CharField(max_length=63)

    def __str__(self):
        return self.name


class Train(models.Model):
    name = models.CharField(max_length=63)
    cargo_num = models.IntegerField()
    places_in_cargo = models.IntegerField()
    train_type = models.ForeignKey(TrainType, related_name="trains",
                                   on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Crew(models.Model):
    first_name = models.CharField(max_length=63)
    last_name = models.CharField(max_length=63)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Journey(models.Model):
    route = models.ForeignKey(Route, related_name="journeys",
                              on_delete=models.CASCADE)
    train = models.ForeignKey(Train, related_name="journeys",
                              on_delete=models.CASCADE)
    departure_time = models.DateTimeField()
    arrival_time = models.DateTimeField()
    crew = models.ManyToManyField(Crew,
                                  related_name="journeys")

    class Meta:
        ordering = ["-departure_time"]

    def __str__(self):
        return f"{self.route} [{self.departure_time}]"


class Order(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, related_name="orders",
                             on_delete=models.CASCADE)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Order {self.id} by {self.user.username}"


class Ticket(models.Model):
    cargo = models.IntegerField()
    seat = models.PositiveIntegerField()
    journey = models.ForeignKey(Journey, related_name="tickets",
                                on_delete=models.CASCADE)
    order = models.ForeignKey(Order, related_name="tickets",
                              on_delete=models.CASCADE)

    class Meta:
        unique_together = ("journey", "cargo", "seat")
        ordering = ["cargo", "seat"]

    def __str__(self):
        return f"Journey: {self.journey.id} | Cargo: {self.cargo} | Seat: {self.seat}"
