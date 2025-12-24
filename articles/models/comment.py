import uuid
from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from articles.base import TimeStampedModel
from constants import MAX_LENGTH_SLUG

class Comment(TimeStampedModel):
  id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
  
  article = models.ForeignKey(
    'Article',
    on_delete=models.CASCADE,
    related_name='comments'
  )
  author = models.ForeignKey(
    User,
    on_delete=models.RESTRICT,
    related_name='comments'
  )
  
  content = models.TextField()
  slug = models.SlugField(max_length=MAX_LENGTH_SLUG, unique=True, db_index=True)
  
  class Meta:
      ordering = ['-created_at']
  
  def save(self, *args, **kwargs):
    if not self.slug:
      self.slug = slugify(self.content[:50])
    super().save(*args, **kwargs)

  def __str__(self):
    return f"Comment by {self.author} on {self.article}"
