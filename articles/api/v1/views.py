from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.db.models import Q
from articles.models import Article
from .serializers import ArticleSerializer
from .permissions import IsAuthorOrReadOnly

class ArticleViewSet(viewsets.ModelViewSet):
  serializer_class = ArticleSerializer
  lookup_field = 'slug'
  permission_classes = [IsAuthorOrReadOnly]
  
  def get_object(self):
    slug = self.kwargs.get('slug')
    obj = get_object_or_404(Article, slug=slug)
    return obj
  
  def get_queryset(self):
    queryset = Article.objects.all()
    
    tag = self.request.query_params.get('tag', None)
    if tag:
      queryset = queryset.filter(tags__name=tag)
    
    author = self.request.query_params.get('author', None)
    if author:
      queryset = queryset.filter(author__username=author)
    
    return queryset
  
  def perform_create(self, serializer):
    serializer.save(author=self.request.user)
  
  @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
  def favorite(self, request, slug=None):
    article = self.get_object()
    user = request.user
    
    if article.favorited_by.filter(pk=user.pk).exists():
      return Response(
        {"detail": "This article is already favorited."},
        status=status.HTTP_400_BAD_REQUEST
      )
    
    article.favorited_by.add(user)
    return Response(
      {"detail": "Article added to favorites successfully."},
      status=status.HTTP_201_CREATED
    )
  
  @action(detail=True, methods=['delete'], permission_classes=[IsAuthenticated])
  def unfavorite(self, request, slug=None):
    article = self.get_object()
    user = request.user
    
    if not article.favorited_by.filter(pk=user.pk).exists():
      return Response(
        {"detail": "This article is not in your favorites."},
        status=status.HTTP_400_BAD_REQUEST
      )
    
    article.favorited_by.remove(user)
    return Response(
      {"detail": "Article removed from favorites successfully."},
      status=status.HTTP_204_NO_CONTENT
    )
  
  @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
  def like(self, request, slug=None):
    article = self.get_object()
    user = request.user
    
    if article.liked_by.filter(pk=user.pk).exists():
      return Response(
        {"detail": "You have already liked this article."},
        status=status.HTTP_400_BAD_REQUEST
      )
    
    article.liked_by.add(user)
    return Response(
      {"detail": "Article liked successfully.", "likes_count": article.liked_by.count()},
      status=status.HTTP_201_CREATED
    )
  
  @action(detail=True, methods=['delete'], permission_classes=[IsAuthenticated])
  def unlike(self, request, slug=None):
    article = self.get_object()
    user = request.user
    
    if not article.liked_by.filter(pk=user.pk).exists():
      return Response(
        {"detail": "You have not liked this article."},
        status=status.HTTP_400_BAD_REQUEST
      )
    
    article.liked_by.remove(user)
    return Response(
      {"detail": "Article unliked successfully.", "likes_count": article.liked_by.count()},
      status=status.HTTP_204_NO_CONTENT
    )

