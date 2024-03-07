from rest_framework import serializers
from sales.models import Address, Item, Acquisition
from products.serializers import ProductSerializer


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ['id', 'cep', 'uf', 'city', 'name', 'neighborhood']


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ['id', 'product', 'price']

    product = ProductSerializer(read_only=True)


class AcquisitionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Acquisition
        fields = ['id', 'price', 'date', 'status', 'address', 'items']

    address = AddressSerializer(read_only=True)
    items = ItemSerializer(many=True, read_only=True)