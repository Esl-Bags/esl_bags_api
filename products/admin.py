from django.contrib import admin
from products.models import Brand, Product, Carousel

# Register your models here.
admin.site.register(Brand)
admin.site.register(Product)
admin.site.register(Carousel)