from rest_framework import serializers
from ....models import Comment
from .user_serializer import UserProfileSerializer

class CommentSerializer(serializers.ModelSerializer):
  author = UserProfileSerializer(read_only=True)

  class Meta:
    model = Comment
    fields = ['id', 'article', 'author', 'content', 'created_at']
