from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django.shortcuts import get_object_or_404
from articles.models import Article
from .serializers import ArticleSerializer

class ArticleViewSet(viewsets.ModelViewSet):
  serializer_class = ArticleSerializer
  lookup_field = 'slug'
  permission_classes = [IsAuthenticatedOrReadOnly]
  
  def get_object(self):
    slug = self.kwargs.get('slug')
    obj = get_object_or_404(Article, slug=slug)
    return obj
  
  def get_queryset(self):
    return Article.objects.all()
  
  def perform_create(self, serializer):
    serializer.save(author=self.request.user)
