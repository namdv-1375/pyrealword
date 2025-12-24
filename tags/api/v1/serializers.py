from rest_framework import serializers
from tags.models import Tag

class TagSerializer(serializers.ModelSerializer):
  class Meta:
    model = Tag
    fields = ['id', 'name', 'slug', 'description', 'created_at', 'updated_at']
