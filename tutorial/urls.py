from django.contrib import admin
from django.urls import path, include

urlpatterns = [
  path('admin/', admin.site.urls),
  path('api/v1/auth/', include('authentication.api.v1.urls')),
  path('api/v1/users/', include('users.api.v1.urls')),
  path('api/v1/tags/', include('tags.api.v1.urls')),
  path('api/v1/articles/', include('articles.api.v1.urls')),
]
