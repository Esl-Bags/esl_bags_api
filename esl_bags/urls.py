from django.contrib import admin
from django.urls import include, path, re_path
from django.conf.urls.static import static
from django.conf import settings
from django.views.static import serve 


urlpatterns = [
    path('user/', include("accounts.urls")),
    path('admin/', admin.site.urls),
    re_path(r'^static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT}),
]

# urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)