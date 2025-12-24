from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from django.shortcuts import get_object_or_404
from articles.models import Comment, Article
from .serializers import CommentSerializer
from ..permissions import IsCommentAuthorOrReadOnly

class CommentViewSet(viewsets.ModelViewSet):
  serializer_class = CommentSerializer
  permission_classes = [IsCommentAuthorOrReadOnly]
  
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
  
  def update(self, request, *args, **kwargs):
    instance = self.get_object()
    if instance.author != request.user:
      from rest_framework.exceptions import PermissionDenied
      raise PermissionDenied("You do not have permission to edit this comment.")
    return super().update(request, *args, **kwargs)
  
  def destroy(self, request, *args, **kwargs):
    instance = self.get_object()
    if instance.author != request.user:
      from rest_framework.exceptions import PermissionDenied
      raise PermissionDenied("You do not have permission to delete this comment.")
    return super().destroy(request, *args, **kwargs)

