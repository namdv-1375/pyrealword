from rest_framework import serializers
from articles.models import Article, Comment
from tags.api.v1.serializers import TagSerializer
from users.api.v1.serializers import UserProfileSerializer

class ArticleSerializer(serializers.ModelSerializer):
  tags = TagSerializer(many=True, read_only=True)
  author = UserProfileSerializer(read_only=True)

  class Meta:
    model = Article
    fields = ['id', 'title', 'slug', 'content', 'author', 'tags', 'created_at', 'updated_at']

class CommentSerializer(serializers.ModelSerializer):
  author = UserProfileSerializer(read_only=True)

  class Meta:
    model = Comment
    fields = ['id', 'article', 'author', 'content', 'slug', 'created_at', 'updated_at']
