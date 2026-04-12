from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    def __str__(self):
        return (f"username: {self.username}; email: {self.email}")


class Order(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, blank=False, null=False, on_delete=models.CASCADE)


class Ticket(models.Model):
    cargo = models.IntegerField()
    seat = models.PositiveIntegerField()
    journey = models.ManyToManyField("Journey")
    order = models.ForeignKey(Order, blank=False, null=False, on_delete=models.CASCADE)
