from rest_framework import serializers
from django.contrib.auth.hashers import make_password

from django.contrib.auth.models import User
from esl_bags.models import Acquisition, Address, Item, Product, Brand, Car
from esl_bags.validations import emailValidate, valueBlankValidate, containsFourCharacters

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
        fields = ['id', 'email', 'first_name', 'is_staff', 'acquisitions', 'car', 'addresses' ]
        read_only_fields = ['is_staff']

    email = serializers.CharField(max_length=80, allow_blank=True)
    first_name = serializers.CharField(max_length=40)
    acquisitions = AcquisitionSerializer(many=True, read_only=True)
    car = CarSerializer(many=True, read_only=True)
    addresses = AddressSerializer(many=True, read_only=True)

    def validate_email(self, value):
        """
        Check if value is a valide e-mail address.
        """
        if valueBlankValidate(value):
            raise serializers.ValidationError("O e-mail é obrigatorio.")

        if emailValidate(value):
            raise serializers.ValidationError("Entre com um endereço de e-mail valido.")

        if emailInUse(value):
            raise serializers.ValidationError("O e-mail já é usado.")

        return value

    def validate_first_name(self, value):
        """
        Check the name field.
        """
        if valueBlankValidate(value):
            raise serializers.ValidationError("O nome é obrigatorio.")

        if not containsFourCharacters(value):
            raise serializers.ValidationError("O nome deve conter pelo menos 4 caracteres.")

        return value

    def update(self, instance, validated_data):
        instance.username = validated_data.get('email', instance.username)
        instance.email = validated_data.get('email', instance.username)
        instance.first_name = validated_data.get('first_name', instance.first_name)

        instance.save()
        return instance


class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [ 'email', 'first_name', 'password' ]
        extra_kwargs = {'password': {'write_only': True}}

    email = serializers.CharField(max_length=80, allow_blank=True)
    first_name = serializers.CharField(max_length=40, allow_blank=True)
    password = serializers.CharField(max_length=40, allow_blank=True)

    def validate_email(self, value):
        """
        Check if value is a valide e-mail address.
        """
        if valueBlankValidate(value):
            raise serializers.ValidationError("O e-mail é obrigatorio.")

        if emailValidate(value):
            raise serializers.ValidationError("Entre com um endereço de e-mail valido.")

        if emailInUse(value):
            raise serializers.ValidationError("O e-mail já é usado.")

        return value

    def validate_first_name(self, value):
        """
        Check the name field.
        """
        if valueBlankValidate(value):
            raise serializers.ValidationError("O nome é obrigatorio.")

        if not containsFourCharacters(value):
            raise serializers.ValidationError("O nome deve conter pelo menos 4 caracteres.")

        return value

    def validate_password(self, value):
        """
        Check password.
        """
        if valueBlankValidate(value):
            raise serializers.ValidationError("A senha é obrigatoria.")

        if not containsFourCharacters(value):
            raise serializers.ValidationError("A senha deve conter pelo menos 4 caracteres.")

    def create(self, validated_data):
        validated_data['username'] = validated_data['email']
        validated_data['password'] = make_password(validated_data['password'])
        return User.objects.create(**validated_data)


def emailInUse(email):
    user = User.objects.filter(username=email)
    if len(user) > 0:
        return True
    return False


class AuthTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    email = serializers.CharField(max_length=80, allow_blank=True)

    def validate(self, data):
        user_obj = None
        email = data.get('email')
        password = data.get('password')
        if email and password:
            user_obj = User.objects.filter(email=email).first()
            if emailValidate(email):
                raise serializers.ValidationError("Entre com um endereço de e-mail valido.")
            if not user_obj:
                raise serializers.ValidationError("E-mail não encontrado.")
            if not user_obj.check_password(password):
                raise serializers.ValidationError("E-mail ou senha incorretos.")
        return data

    def create(self, validated_data):
        user = User.objects.get(email=validated_data['email'])
        refresh = RefreshToken.for_user(user)
        return {
            'user': user,
            'token': str(refresh.access_token)
        }