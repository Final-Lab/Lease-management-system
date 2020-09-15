from django.db import models
from django.contrib.auth.models import User


class EmailValid(models.Model):
    email = models.CharField(max_length=255)
    sec_code = models.CharField(max_length=255)

    def __str__(self):
        return self.email


class Inventory(models.Model):
    name = models.CharField(max_length=255)
    status = models.CharField(max_length=255)
    supplier = models.ForeignKey(User, default=1, on_delete=models.CASCADE,)

    def __str__(self):
        return self.name


class RentalRecord(models.Model):
    student = models.CharField(max_length=255)
    status = models.CharField(max_length=255)
    item = models.ForeignKey(Inventory, default=1, on_delete=models.CASCADE,)
    reason = models.CharField(max_length=255)


class RentApplication(models.Model):
    student = models.ForeignKey(User,  on_delete=models.CASCADE, blank=True, null=True)
    status = models.CharField(max_length=255,blank=True, null=True)
    item = models.ForeignKey(Inventory,  on_delete=models.CASCADE, blank=True, null=True)
    reason = models.CharField(max_length=255,blank=True, null=True)
    date = models.DateField(auto_now_add=True, blank=True, null=True)
    type = models.CharField(max_length=255,blank=True, null=True)
    def __str__(self):
        return self.status


class SupplyAplication(models.Model):
    student = models.ForeignKey(User, default=1, on_delete=models.CASCADE, )
    status = models.CharField(max_length=255)
