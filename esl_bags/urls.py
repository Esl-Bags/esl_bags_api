from django.contrib import admin
from django.urls import include, path, re_path
from django.conf import settings
from django.views.static import serve 


urlpatterns = [
    path('user/', include("accounts.urls")),
    path('product/', include("products.urls")),
    path('admin/', admin.site.urls),
    re_path(r'^static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT}),
    re_path(r'^media/(?P<path>.*)$', serve,{'document_root': settings.MEDIA_ROOT}),
]