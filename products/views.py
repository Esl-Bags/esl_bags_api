from rest_framework.response import Response
from rest_framework.permissions import BasePermission, IsAdminUser
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, DestroyAPIView
from rest_framework import status
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters

from products.models import Brand, Offer, Product
from products.serializers import BrandSerializer, OfferSerializer, OfferCreateDestroySerializer, ProductSerializer
from esl_bags.utils import MethodSerializerView


class IsGetMethodOrAuthenticated(BasePermission):
    def has_permission(self, request, view):
        if request.method == 'GET':
            return True
        if bool(request.user and request.user.is_authenticated):
            return True
        return False
    
class IsGetMethodOrStaffUser(BasePermission):
    def has_permission(self, request, view):
        if request.method == 'GET':
            return True
        if bool(request.user and request.user.is_authenticated and request.user.is_staff):
            return True
        return False
    


# Create your views here.
class BrandCreateList(ListCreateAPIView):
    queryset = Brand.objects.filter(is_active=True)
    serializer_class = BrandSerializer
    permission_classes = [IsGetMethodOrAuthenticated]

    def post(self, request, format=None):
        if not request.user.is_staff:
            return Response({'detail': 'Usuário não tem permissão para cadastro de marcas.'}, status=status.HTTP_400_BAD_REQUEST)
        brand = BrandSerializer(data=request.data)
        if brand.is_valid():
            brand_obj = Brand.objects.filter(name=request.data['name']).first()
            if brand_obj:
                brand_obj.is_active = True
                brand_obj.save()
            else:
                brand.save()
            return Response(brand.data, status=status.HTTP_201_CREATED)
        return Response(brand.errors, status=status.HTTP_400_BAD_REQUEST)
    

class BrandUpdateDelete(RetrieveUpdateDestroyAPIView):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer
    permission_classes = [IsGetMethodOrAuthenticated]

    def patch(self, request, pk):
        if not request.user.is_staff:
            return Response({'detail': 'Usuário não tem permissão para atualizar marcas.'}, status=status.HTTP_400_BAD_REQUEST)
        brand_obj = Brand.objects.get(id=pk)
        brand = BrandSerializer(brand_obj, data=request.data, partial=True)
        if brand.is_valid():
            brand.save()
            return Response(brand.data, status=status.HTTP_201_CREATED)
        return Response(brand.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk, format=None):
        if not request.user.is_staff:
            return Response({'detail': 'Usuário não tem permissão para deletar marcas.'}, status=status.HTTP_400_BAD_REQUEST)
        brand = Brand.objects.get(id=pk)
        brand.is_active = False
        brand.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ProductCreateList(ListCreateAPIView):
    queryset = Product.objects.filter(is_active=True)
    serializer_class = ProductSerializer
    permission_classes = [IsGetMethodOrAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['brand']
    search_fields = ['name', 'description']


    def post(self, request, format=None):
        if not request.user.is_staff:
            return Response({'detail': 'Usuário não tem permissão para cadastro de produtos.'}, status=status.HTTP_400_BAD_REQUEST)
        product = ProductSerializer(data=request.data)
        if product.is_valid():
            brand = product.validated_data['brand']
            product_obj = Product.objects.filter(name=request.data['name'], brand=brand).first()
            if product_obj:
                product_obj.is_active = True
                product_obj.save()
            else:
                product.save()
            return Response(product.data, status=status.HTTP_201_CREATED)
        return Response(product.errors, status=status.HTTP_400_BAD_REQUEST)
    

class ProductUpdateDelete(RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsGetMethodOrAuthenticated]

    def patch(self, request, pk):
        if not request.user.is_staff:
            return Response({'detail': 'Usuário não tem permissão para atualizar produtos.'}, status=status.HTTP_400_BAD_REQUEST)
        
        product_obj = Product.objects.get(id=pk)
        product = ProductSerializer(product_obj, data=request.data, partial=True)
        if product.is_valid():
            product.save()
            return Response(product.data, status=status.HTTP_201_CREATED)
        return Response(product.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk, format=None):
        if not request.user.is_staff:
            return Response({'detail': 'Usuário não tem permissão para deletar produtos.'}, status=status.HTTP_400_BAD_REQUEST)
        product = Product.objects.get(id=pk)
        product.is_active = False
        product.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

class OfferListCreate(MethodSerializerView, ListCreateAPIView):
    queryset = Offer.objects.all()
    method_serializer_classes = {
        ('GET'): OfferSerializer,
        ('POST'): OfferCreateDestroySerializer
    }
    permission_classes = [IsGetMethodOrAuthenticated]


class OfferDestory(DestroyAPIView):
    queryset = Offer.objects.all()
    serializer_class = OfferSerializer
    permission_classes = [IsAdminUser]