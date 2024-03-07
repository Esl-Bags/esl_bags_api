from django.db import models

# Create your models here.

class Car(models.Model):
    product = models.ForeignKey('products.Product', on_delete=models.CASCADE)
    user = models.ForeignKey('auth.User', related_name='car', on_delete=models.CASCADE)