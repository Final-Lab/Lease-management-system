from django.contrib import admin
from .models import Inventory, SupplyAplication ,RentApplication

admin.site.register(Inventory)
admin.site.register(RentApplication)
admin.site.register(SupplyAplication)
# Register your models here.
