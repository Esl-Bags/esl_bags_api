from django.urls import path
from products import views

urlpatterns = [
    path('brand/', views.BrandCreateList.as_view()),
    path('brand/<int:pk>/', views.BrandUpdateDelete.as_view())
]
