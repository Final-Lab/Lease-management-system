from django.contrib import admin
from .models import MyUser, Inventory, RentalRecord

admin.site.register(MyUser)
admin.site.register(Inventory)
admin.site.register(RentalRecord)

# Register your models here.
