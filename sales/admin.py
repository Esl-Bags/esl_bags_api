from django.contrib import admin
from sales.models import Address, Acquisition, Item

# Register your models here.
admin.site.register(Address)
admin.site.register(Acquisition)
admin.site.register(Item)