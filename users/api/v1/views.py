from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from users.models import Follow
from .serializers import UserProfileSerializer

class UserViewSet(viewsets.ReadOnlyModelViewSet):
  serializer_class = UserProfileSerializer
  lookup_field = 'username'
  
  def get_object(self):
    username = self.kwargs.get('username')
    obj = get_object_or_404(User, username=username)
    return obj
  
  @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
  def follow(self, request, username=None):
    user_to_follow = self.get_object()
    current_user = request.user
    
    if user_to_follow == current_user:
      return Response(
        {"detail": "You cannot follow yourself."},
        status=status.HTTP_400_BAD_REQUEST
      )
    
    if Follow.objects.filter(follower=current_user, following=user_to_follow).exists():
      return Response(
        {"detail": "You are already following this user."},
        status=status.HTTP_400_BAD_REQUEST
      )
    
    Follow.objects.create(follower=current_user, following=user_to_follow)
    return Response(
      {"detail": "You are now following this user."},
      status=status.HTTP_201_CREATED
    )
  
  @action(detail=True, methods=['delete'], permission_classes=[IsAuthenticated])
  def unfollow(self, request, username=None):
    user_to_unfollow = self.get_object()
    current_user = request.user
    
    follow_exists = Follow.objects.filter(
      follower=current_user,
      following=user_to_unfollow
    ).exists()
    
    if not follow_exists:
      return Response(
        {"detail": "You are not following this user."},
        status=status.HTTP_400_BAD_REQUEST
      )
    
    Follow.objects.filter(
      follower=current_user,
      following=user_to_unfollow
    ).delete()

    return Response(
      {"detail": "You have unfollowed this user."},
      status=status.HTTP_204_NO_CONTENT
    )
