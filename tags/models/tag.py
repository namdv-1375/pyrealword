import uuid
from django.db import models
from django.utils.text import slugify
from tags.base import TimeStampedModel
from constants import MAX_LENGTH_NAME, MAX_LENGTH_SLUG

class Tag(TimeStampedModel):
  id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
  name = models.CharField(
    max_length=MAX_LENGTH_NAME,
    unique=True,
    db_index=True
  )
  slug = models.SlugField(
    max_length=MAX_LENGTH_SLUG,
    unique=True,
    db_index=True
  )
  description = models.TextField(
    blank=True,
    null=True
  )
  
  class Meta:
    ordering = ['name']
    indexes = [
      models.Index(fields=['slug']),
      models.Index(fields=['name']),
    ]
  
  def save(self, *args, **kwargs):
    if not self.slug:
      self.slug = slugify(self.name)
    super().save(*args, **kwargs)

  def __str__(self):
    return self.name
