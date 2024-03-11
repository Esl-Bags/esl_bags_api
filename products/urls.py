from django.urls import path
from products import views

urlpatterns = [
    path('', views.ProductCreateList.as_view()),
    path('<int:pk>/', views.ProductUpdateDelete.as_view()),
    path('brand/', views.BrandCreateList.as_view()),
    path('brand/<int:pk>/', views.BrandUpdateDelete.as_view()),
    path('offer/', views.OfferListCreate.as_view()),
    path('offer/<int:pk>/', views.OfferDestroy.as_view()),
    path('carousel/', views.CarouselListCreate.as_view()),
    path('carousel/<int:pk>/', views.CarouselDestroy.as_view())
]
