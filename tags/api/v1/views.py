from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from tags.models import Tag
from .serializers import TagSerializer

class TagViewSet(viewsets.ModelViewSet):
  queryset = Tag.objects.all()
  serializer_class = TagSerializer
  lookup_field = 'slug'
  permission_classes = [IsAuthenticatedOrReadOnly]
