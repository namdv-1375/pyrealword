from rest_framework import serializers
from articles.models import Comment
from users.api.v1.serializers import UserProfileSerializer

class CommentSerializer(serializers.ModelSerializer):
  author = UserProfileSerializer(read_only=True)
  can_edit = serializers.SerializerMethodField()
  can_delete = serializers.SerializerMethodField()

  class Meta:
    model = Comment
    fields = ['id', 'article', 'author', 'content', 'slug', 'created_at', 'updated_at', 'can_edit', 'can_delete']
    read_only_fields = ['article', 'slug']
  
  def get_can_edit(self, obj):
    request = self.context.get('request')
    if not request or not request.user.is_authenticated:
      return False
    return obj.author == request.user
  
  def get_can_delete(self, obj):
    request = self.context.get('request')
    if not request or not request.user.is_authenticated:
      return False
    return obj.author == request.user
