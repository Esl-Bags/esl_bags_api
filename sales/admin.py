from django.contrib import admin
from sales.models import Address, Acquisition, Item, Car

# Register your models here.
admin.site.register(Address)
admin.site.register(Acquisition)
admin.site.register(Item)
admin.site.register(Car)