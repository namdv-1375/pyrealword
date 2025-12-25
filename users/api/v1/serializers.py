from rest_framework import serializers
from django.contrib.auth.models import User
from users.models import Follow

class UserFollowStatsMixin:
  def get_followers_count(self, obj):
    return Follow.objects.filter(following=obj).count()
  
  def get_following_count(self, obj):
    return Follow.objects.filter(follower=obj).count()
  
  def get_is_followed(self, obj):
    request = self.context.get('request')
    if request and request.user.is_authenticated:
      return Follow.objects.filter(
        follower=request.user,
        following=obj
      ).exists()

    return False

class UserProfileSerializer(UserFollowStatsMixin, serializers.ModelSerializer):
  followers_count = serializers.SerializerMethodField()
  following_count = serializers.SerializerMethodField()
  is_followed = serializers.SerializerMethodField()
  
  class Meta:
    model = User
    fields = ['id', 'username', 'email', 'first_name', 'last_name', 'followers_count', 'following_count', 'is_followed']

class UserDetailSerializer(UserFollowStatsMixin, serializers.ModelSerializer):
  followers_count = serializers.SerializerMethodField()
  following_count = serializers.SerializerMethodField()
  is_followed = serializers.SerializerMethodField()
  
  class Meta:
    model = User
    fields = ['id', 'username', 'email', 'first_name', 'last_name', 'followers_count', 'following_count', 'is_followed']

