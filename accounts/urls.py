from django.urls import include, path
from rest_framework.authtoken import views as auth_views
from . import views

#teste github actions
urlpatterns = [
    path('', views.UserRetriveCreate.as_view()),
    path('login/', views.AuthLoginUser.as_view()),
    path('change-password/', views.PasswordUpdate.as_view()),
    path('forget-password/', include('django_rest_passwordreset.urls', namespace='password_reset')),
    path('api-auth/', include('rest_framework.urls')),
]
