from django.db import models

# Create your models here.
class Brand(models.Model):
    name = models.CharField(max_length=30)
    is_active = models.BooleanField(blank=True, default=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=40)
    brand = models.ForeignKey('Brand', related_name='products', on_delete=models.CASCADE)
    photo = models.ImageField(upload_to = 'media/images/products')
    description = models.CharField(max_length=80)
    price = models.FloatField()
    is_active = models.BooleanField(blank=True, default=True)