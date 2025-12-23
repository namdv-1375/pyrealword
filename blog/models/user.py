from django.db import models
from django.contrib.auth.models import User
from .base import TimeStampedModel


class UserProfile(TimeStampedModel):
  user = models.OneToOneField(
    User,
    on_delete=models.CASCADE,
    related_name='profile'
  )
  
  bio = models.TextField(blank=True, null=True)
  avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
  
  class Meta:
    verbose_name = 'User Profile'
    verbose_name_plural = 'User Profiles'
