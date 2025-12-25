from django.urls import path
from .views import UserViewSet

urlpatterns = [
  path('<str:username>/', UserViewSet.as_view({
    'get': 'retrieve'
  }), name='profile-detail'),
  path('<str:username>/follow/', UserViewSet.as_view({
    'post': 'follow'
  }), name='profile-follow'),
  path('<str:username>/unfollow/', UserViewSet.as_view({
    'delete': 'unfollow'
  }), name='profile-unfollow'),
]
