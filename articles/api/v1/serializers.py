from rest_framework import serializers
from articles.models import Article, Comment
from tags.api.v1.serializers import TagSerializer
from users.api.v1.serializers import UserProfileSerializer

class ArticleSerializer(serializers.ModelSerializer):
  tags = TagSerializer(many=True, read_only=True)
  author = UserProfileSerializer(read_only=True)
  favorited = serializers.SerializerMethodField()
  favorites_count = serializers.SerializerMethodField()
  is_liked = serializers.SerializerMethodField()
  likes_count = serializers.SerializerMethodField()

  class Meta:
    model = Article
    fields = ['id', 'title', 'slug', 'content', 'author', 'tags', 'favorited', 'favorites_count', 'is_liked', 'likes_count', 'created_at', 'updated_at']
  
  def get_favorited(self, obj):
    request = self.context.get('request')
    if request and request.user.is_authenticated:
      return obj.favorited_by.filter(pk=request.user.pk).exists()
    return False
  
  def get_favorites_count(self, obj):
    return obj.favorited_by.count()
  
  def get_is_liked(self, obj):
    request = self.context.get('request')
    if request and request.user.is_authenticated:
      return obj.liked_by.filter(pk=request.user.pk).exists()
    return False
  
  def get_likes_count(self, obj):
    return obj.liked_by.count()

class CommentSerializer(serializers.ModelSerializer):
  author = UserProfileSerializer(read_only=True)

  class Meta:
    model = Comment
    fields = ['id', 'article', 'author', 'content', 'slug', 'created_at', 'updated_at']
