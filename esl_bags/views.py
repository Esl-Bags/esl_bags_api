from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import BasePermission
from rest_framework.views import APIView
from rest_framework import status

from esl_bags.serializers import UserSerializer, UserCreateSerializer


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
