from rest_framework import serializers
from django.contrib.auth.hashers import make_password

from django.contrib.auth.models import User
from esl_bags.models import Acquisition, Address, Item, Product, Brand, Car

class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ['id', 'cep', 'uf', 'city', 'name', 'neighborhood']


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ['name']


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'photo', 'description', 'price', 'brand']

    brand = BrandSerializer(read_only=True)


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


class CarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Car
        fields = ['product']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'password', 'is_staff', 'acquisitions', 'car', 'addresses' ]
        read_only_fields = ['is_staff']
        extra_kwargs = {'password': {'write_only': True}}

    username = serializers.EmailField()
    first_name = serializers.CharField(max_length=40)
    acquisitions = AcquisitionSerializer(many=True, read_only=True)
    car = CarSerializer(many=True, read_only=True)
    addresses = AddressSerializer(many=True, read_only=True)

    def create(self, validated_data):
        validated_data['email'] = validated_data['username']
        validated_data['password'] = make_password(validated_data['password'])
        return User(**validated_data)

    def update(self, instance, validated_data):
        instance.username = validated_data.get('username', instance.username)
        instance.email = validated_data.get('username', instance.username)
        instance.first_name = validated_data.get('first_name', instance.first_name)

        password = validated_data.get('password')

        if password:
            instance.password = make_password(password)

        instance.save()
        return instance
