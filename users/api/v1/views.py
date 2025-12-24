from rest_framework import viewsets
from rest_framework.decorators import action
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from .serializers import UserProfileSerializer

class UserViewSet(viewsets.ReadOnlyModelViewSet):
  serializer_class = UserProfileSerializer
  lookup_field = 'username'
  
  def get_object(self):
    username = self.kwargs.get('username')
    obj = get_object_or_404(User, username=username)
    return obj
