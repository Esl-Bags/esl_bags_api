from django.urls import path
from products import views

urlpatterns = [
    path('brand/', views.BrandCreateList.as_view())
]
