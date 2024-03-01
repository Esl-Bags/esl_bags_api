from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import BasePermission
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework import status

from products.models import Brand
from products.serializers import BrandSerializer


class IsGetMethodOrAuthenticated(BasePermission):
    def has_permission(self, request, view):
        if request.method == 'GET':
            return True
        if bool(request.user and request.user.is_authenticated):
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

    def path(self, request, format=None):
        if not request.user.is_staff:
            return Response({'detail': 'Usuário não tem permissão para atualizar marcas.'}, status=status.HTTP_400_BAD_REQUEST)
        brand = BrandSerializer(data=request.data)
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