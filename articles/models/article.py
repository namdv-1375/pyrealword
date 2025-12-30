import uuid
from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from articles.base import TimeStampedModel
from tags.models import Tag
from constants import MAX_LENGTH_TITLE, MAX_LENGTH_SLUG

class Article(TimeStampedModel):
  id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
  title = models.CharField(max_length=MAX_LENGTH_TITLE, unique=True, db_index=True)
  slug = models.SlugField(max_length=MAX_LENGTH_SLUG, unique=True, db_index=True)
  content = models.TextField()
  author = models.ForeignKey(User, on_delete=models.RESTRICT, related_name='articles')
  tags = models.ManyToManyField(Tag, related_name='articles', blank=True)
  favorited_by = models.ManyToManyField(User, related_name='favorite_articles', blank=True)
  liked_by = models.ManyToManyField(User, related_name='liked_articles', blank=True)
  
  class Meta:
    ordering = ['-created_at']
    indexes = [
      models.Index(fields=['author']),
      models.Index(fields=['title']),
      models.Index(fields=['slug']),
    ]
  
  def save(self, *args, **kwargs):
    if not self.slug:
      self.slug = slugify(self.title)
    super().save(*args, **kwargs)
  
  def __str__(self):
    return self.title
