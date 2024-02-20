from django.contrib import admin
from django.urls import include, path


urlpatterns = [
    path('', include("esl_bags.urls")),
    path('admin/', admin.site.urls),
]
