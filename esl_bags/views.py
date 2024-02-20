from rest_framework.response import Response
from rest_framework import generics
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, BasePermission
from rest_framework.views import APIView
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework import status

from esl_bags.serializers import UserSerializer
from django.contrib.auth.models import User


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
        user = UserSerializer(data=request.data)
        if user.is_valid():
            user.save()
            return Response(user.data, status=status.HTTP_201_CREATED)
        return Response(user.errors, status=status.HTTP_400_BAD_REQUEST)

