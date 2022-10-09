from django.urls import include, path
from django.contrib import admin

urlpatterns = [
    path('', include('django_prometheus.urls')),
    path('admin/', admin.site.urls),
    path('api/', include('api.urls'))
]
