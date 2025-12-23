import uuid
from django.db import models
from django. contrib.auth.models import User
from django.utils.text import slugify
from .base import TimeStampedModel
from .article import Article
from ..constants import MAX_LENGTH_SLUG

class Comment(TimeStampedModel):
  id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
  
  article = models.ForeignKey(
      Article,
      on_delete=models.CASCADE,
      related_name='comments'
  )
  author = models.ForeignKey(
      User,
      on_delete=models.CASCADE,
      related_name='comments'
  )
  
  content = models. TextField()
  slug = models.SlugField(max_length=MAX_LENGTH_SLUG, unique=True, db_index=True)
  
  class Meta:
      ordering = ['-created_at']
  
  def save(self, *args, **kwargs):
    if not self.slug:
      base_slug = f"{self.author.username}-{self.article.slug}"
      self.slug = slugify(base_slug)
    super().save(*args, **kwargs)
