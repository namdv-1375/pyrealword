from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from django.shortcuts import get_object_or_404
from articles.models import Comment, Article
from .serializers import CommentSerializer
from ..permissions import IsAuthorOrReadOnly

class CommentViewSet(viewsets.ModelViewSet):
  serializer_class = CommentSerializer
  permission_classes = [IsAuthorOrReadOnly]
  
  def get_object(self):
    pk = self.kwargs.get('pk')
    slug = self.kwargs.get('slug')
    obj = get_object_or_404(Comment, pk=pk, article__slug=slug)
    return obj
  
  def get_queryset(self):
    article_slug = self.kwargs.get('slug')
    get_object_or_404(Article, slug=article_slug)
    return Comment.objects.filter(article__slug=article_slug)
  
  def perform_create(self, serializer):
    article_slug = self.kwargs.get('slug')
    article = get_object_or_404(Article, slug=article_slug)
    serializer.save(author=self.request.user, article=article)
