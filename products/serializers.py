from rest_framework import serializers
from products.models import Brand, Offer, Product


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ['id', 'name']

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

    brand = serializers.CharField()

    def validate_name(self, value):
        if len(value) < 3:
            raise serializers.ValidationError("O produto deve conter mais de dois caracteres.")
        
        return value
    
    def validate_brand(self, value):
        brand_object = Brand.objects.filter(name=value).first()
        if not brand_object:
            raise serializers.ValidationError("Marca não existe!")
        
        return brand_object
    
    def validate(self, attrs):
        name = attrs.get('name', '')
        brand = attrs.get('brand', '')
        
        if name and brand:
            product = Product.objects.filter(name=name, brand=brand.id, is_active=True)

            if len(product) > 0:
                raise serializers.ValidationError("O produto já foi registrado.")
        
        return attrs

    def create(self, validated_data):
        print('test')
        print(validated_data['brand'])
        return Product.objects.create(**validated_data)
    

class OfferSerializer(serializers.ModelSerializer):
    class Meta:
        model = Offer
        fields = ['id', 'product', 'discount']
        read_only_fields = ['id']

    product = ProductSerializer()
    

class OfferCreateDestroySerializer(serializers.ModelSerializer):
    class Meta:
        model = Offer
        fields = ['id', 'product', 'discount']

    def validate_discount(self, value):
        if value < 0:
            raise serializers.ValidationError("O desconto não pode ser um numero negativo.")
        
        if value == 0:
            raise serializers.ValidationError("O valor do desconto não pode ser zero.")
        
        if value > 100:
            raise serializers.ValidationError("O desconto não pode ser maior que 100%.")    

        return value