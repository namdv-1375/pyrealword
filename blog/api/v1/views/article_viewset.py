from rest_framework import viewsets
from django.shortcuts import get_object_or_404
from ....models import Article
from ..serializers.article_serializer import ArticleSerializer

class ArticleViewSet(viewsets.ModelViewSet):
    serializer_class = ArticleSerializer
    lookup_field = 'slug'
    
    def get_object(self):
        slug = self.kwargs.get('slug')
        obj = get_object_or_404(Article, slug=slug)
        return obj
    
    def get_queryset(self):
        return Article.objects.all()
