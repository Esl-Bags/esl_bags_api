from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import BasePermission
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.authtoken.views import ObtainAuthToken
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from products.models import Product
from accounts.models import Car
from accounts.serializers import UserSerializer, UserCreateSerializer, AuthTokenSerializer, CarSerializer
from products.serializers import ProductSerializer


class IsPostMethodOrAuthenticated(BasePermission):
    def has_permission(self, request, view):
        if request.method == 'POST':
            return True
        if bool(request.user and request.user.is_authenticated):
            return True
        return False


class UserRetriveCreate(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsPostMethodOrAuthenticated]

    def get(self, request, format=None):
        user = UserSerializer(request.user)
        return Response(user.data)

    def post(self, request, format=None):
        user = UserCreateSerializer(data=request.data)
        if user.is_valid():
            user.save()
            return Response(user.data, status=status.HTTP_201_CREATED)
        return Response(user.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, format=None):
        user = request.user
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AuthLoginUser(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = AuthTokenSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            user = User.objects.get(email=serializer.validated_data['email'])
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                'token': token.key,
                'first_name': user.first_name,
                'email': user.email,
                })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PasswordUpdate(APIView):
    permission_classes = [IsAuthenticated]
    def patch(self, request, format=None):
        user = request.user
        data = request.data
        if not user.check_password(data['old_password']):
            return Response({'old_password': 'Senha incorreta.'}, status=status.HTTP_400_BAD_REQUEST)
        if user.check_password(data['new_password']):
            return Response({'new_password': 'A nova senha não pode ser igual a antiga.'}, status=status.HTTP_400_BAD_REQUEST)

        user.set_password(data['new_password'])
        user.save()
        return Response({'status': 'Senha trocada com sucesso.'})


class CarListAdd(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        items = Car.objects.filter(user=request.user)
        product = []
        for item in items:
            product.append(item.product)

        serializer = ProductSerializer(product, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    
    def post(self, request):
        data = { 'user': request.user.id, **request.data}
        car_item = CarSerializer(data=data)
        if car_item.is_valid():
            car_item.save()
            return Response(car_item.data, status=status.HTTP_201_CREATED)
        return Response(car_item.errors, status=status.HTTP_400_BAD_REQUEST)


class CarRemove(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, pk):
        user = request.user
        product = Product.objects.get(id=pk)

        item = Car.objects.filter(user=user, product=product)
        if len(item) > 0:
            item[0].delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response({ 'erro': 'Item não encontrado' }, status=status.HTTP_400_BAD_REQUEST)