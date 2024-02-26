from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import BasePermission
from rest_framework.views import APIView
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from esl_bags.serializers import UserSerializer, UserCreateSerializer, AuthTokenSerializer


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


class ForgetPassword(APIView):
    def post(self, request):
        return Response({'message': 'Mermão, lembra dessa senha ai q eu tô com preguiça de implementar isso.'})


class ResetPassword(APIView):
    authentication_classes = [TokenAuthentication]
    def post(self, request):
        user = request.user
        data = request.data
        if not data['password']:
            Response({'password': 'Esse campo é obrigatório.'}, status=status.HTTP_400_BAD_REQUEST)
        if len(data['password']) < 4:
            pass
