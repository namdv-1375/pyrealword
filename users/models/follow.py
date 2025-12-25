import uuid
from django.db import models
from django.contrib.auth.models import User
from users.base import TimeStampedModel

class Follow(TimeStampedModel):
  id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
  follower = models.ForeignKey(
    User,
    on_delete=models.CASCADE,
    related_name='following'
  )
  following = models.ForeignKey(
    User,
    on_delete=models.CASCADE,
    related_name='followers'
  )
  
  class Meta:
    unique_together = ('follower', 'following')
    indexes = [
      models.Index(fields=['follower']),
      models.Index(fields=['following']),
    ]
  
  def __str__(self):
    return f"{self.follower.username} follows {self.following.username}"
