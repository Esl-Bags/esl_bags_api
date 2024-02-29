from rest_framework import serializers
from products.models import Brand, Product


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ['name']

    def validate_name(self, value):
        brand = Brand.objects.filter(name=value, is_active=True)
        if len(brand) > 0:
            raise serializers.ValidationError("A marca já foi registrada.")
        
        if len(value) < 3:
            raise serializers.ValidationError("A marca deve conter mais de dois caracteres.")
        
        return value


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'photo', 'description', 'price', 'brand']

    brand = BrandSerializer(read_only=True)