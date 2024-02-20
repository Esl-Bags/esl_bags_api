from django.urls import include, path
from rest_framework.generics import CreateAPIView, RetrieveUpdateAPIView
from rest_framework.authtoken import views as auth_views
from django.contrib.auth.models import User
from esl_bags.serializers import UserSerializer
from . import views

urlpatterns = [
    #path('user/', CreateAPIView.as_view(queryset=User.objects.all(), serializer_class=UserSerializer), name='user-create'),
    path('user/', views.UserRetriveCreate.as_view()),
    path('user/login/', auth_views.obtain_auth_token),
    path('api-auth/', include('rest_framework.urls')),
]
