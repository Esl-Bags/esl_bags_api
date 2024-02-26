from django.urls import include, path
from rest_framework.authtoken import views as auth_views
from . import views

urlpatterns = [
    # path('user/', views.UserRetriveCreate.as_view()),
    path('user/login/', views.AuthLoginUser.as_view()),
    # path('user/change-password/', views.PasswordUpdate.as_view()),
    # path('api-auth/', include('rest_framework.urls')),
    # path('user/forget-password/', views.ForgetPassword.as_view()),
    # path('user/password_reset/', include('django_rest_passwordreset.urls', namespace='password_reset')),

]
