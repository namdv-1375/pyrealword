from django.urls import path
from .views import CommentViewSet

urlpatterns = [
    path('', CommentViewSet.as_view({
        'get': 'list',
        'post': 'create'
    }), name='article-comments-list'),
    path('<uuid:pk>/', CommentViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'patch': 'partial_update',
        'delete': 'destroy'
    }), name='article-comments-detail'),
]
