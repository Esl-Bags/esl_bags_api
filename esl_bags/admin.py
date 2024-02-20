from django.contrib import admin
from esl_bags.models import Brand, Product, Address, Acquisition, Item, Car

# Register your models here.
admin.site.register(Brand)
admin.site.register(Product)
admin.site.register(Address)
admin.site.register(Acquisition)
admin.site.register(Item)
admin.site.register(Car)
