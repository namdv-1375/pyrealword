from rest_framework import serializers
from articles.models import Comment
from users.api.v1.serializers import UserProfileSerializer

class CommentSerializer(serializers.ModelSerializer):
  author = UserProfileSerializer(read_only=True)

  class Meta:
    model = Comment
    fields = ['id', 'article', 'author', 'content', 'slug', 'created_at', 'updated_at']
    read_only_fields = ['article']
