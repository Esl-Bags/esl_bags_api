from django.db import models

# Create your models here.

class Brand(models.Model):
    name = models.CharField(max_length=30)
    is_active = models.BooleanField(blank=True, default=True)


class Product(models.Model):
    name = models.CharField(max_length=40)
    brand = models.ForeignKey('Brand', related_name='products', on_delete=models.CASCADE)
    photo = models.ImageField(upload_to = 'media/images/products')
    description = models.CharField(max_length=80)
    price = models.FloatField()
    is_active = models.BooleanField(blank=True, default=True)


class Address(models.Model):
    UFS = {
        'AC': 'Acre',
        'AL': 'Alagoas',
        'AP': 'Amapá',
        'AM': 'Amazonas',
        'BA': 'Bahia',
        'CE': 'Ceará',
        'ES': 'Espírito Santo',
        'GO': 'Goiás',
        'MA': 'Maranhão',
        'MT': 'Mato Grosso',
        'MS': 'Mato Grosso do Sul',
        'MG': 'Minas Gerais',
        'PA': 'Pará',
        'PB': 'Paraíba',
        'PR': 'Paraná',
        'PE': 'Pernambuco',
        'PI': 'Piauí',
        'RJ': 'Rio de Janeiro',
        'RN': 'Rio Grande do Norte',
        'RS': 'Rio Grande do Sul',
        'RO': 'Rondônia',
        'RR': 'Roraima',
        'SC': 'Santa Catarina',
        'SP': 'São Paulo',
        'SE': 'Sergipe',
        'TO': 'Tocantins',
        'DF': 'Distrito Federal',
    }

    cep = models.IntegerField()
    uf = models.CharField(max_length=2, choices=UFS)
    city = models.CharField(max_length=40)
    name = models.CharField(max_length=25)
    neighborhood = models.CharField(max_length=25)
    user = models.ForeignKey('auth.User', related_name='addresses', on_delete=models.CASCADE)
    is_active = models.BooleanField(blank=True, default=True)


class Acquisition(models.Model):
    user = models.ForeignKey('auth.User', related_name='acquisitions', on_delete=models.CASCADE)
    address = models.ForeignKey('Address', on_delete=models.CASCADE)
    price = models.FloatField()
    date = models.DateTimeField()
    status = models.TextChoices("Status", "SOLICITADO CONFIRMADO ENVIADO EM_TRANSITO ENTREGUE CANCELADO")


class Item(models.Model):
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    acquisition = models.ForeignKey('Acquisition', related_name='items', on_delete=models.CASCADE)
    price = models.FloatField()


class Car(models.Model):
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    user = models.ForeignKey('auth.User', related_name='car', on_delete=models.CASCADE)