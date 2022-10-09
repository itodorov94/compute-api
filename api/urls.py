from django.urls import include, path
from rest_framework.authtoken import views as auth_views
from . import views

urlpatterns = [
    path('api-token-auth/', auth_views.obtain_auth_token, name = 'api-token-auth'),
    path('register/', views.RegisterView.as_view(), name = 'register'),
    path('compute/', views.FileUploadView.as_view(), name = 'file-upload')
]
