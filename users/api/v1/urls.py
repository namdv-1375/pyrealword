from django.urls import path
from .views import UserViewSet

urlpatterns = [
  path('<str:username>/', UserViewSet.as_view({
    'get': 'retrieve'
  }), name='profile-detail'),
]
