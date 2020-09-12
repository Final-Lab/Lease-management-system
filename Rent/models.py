from django.db import models
from django.contrib.auth.models import User


class MyUser(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(max_length=500, unique=True)
    username = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    def __str__(self):
        return self.username



class Inventory(models.Model):
    name = models.CharField(max_length=255)
    status = models.CharField(max_length=255)
    supplier = models.ForeignKey(MyUser, default=1, on_delete=models.CASCADE,)

    def __str__(self):
        return self.name


class RentalRecord(models.Model):
    student = models.CharField(max_length=255)
    status = models.CharField(max_length=255)
    item = models.ForeignKey(Inventory, default=1, on_delete=models.CASCADE,)
    reason = models.CharField(max_length=255)
    status = models.CharField(max_length=255)

    def __str__(self):
        return self.status
