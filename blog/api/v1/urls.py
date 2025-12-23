from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView
from .views.user_viewset import UserViewSet
from .views.tag_viewset import TagViewSet
from .views.article_viewset import ArticleViewSet
from .views.comment_viewset import CommentViewSet
from .views.auth_views import RegisterView, LoginView, CurrentUserView

router = DefaultRouter()
router.register(r'tags', TagViewSet, basename='tag')
router.register(r'articles', ArticleViewSet, basename='article')

urlpatterns = [
    path('', include(router.urls)),
    path('auth/register/', RegisterView.as_view(), name='register'),
    path('auth/login/', LoginView.as_view(), name='login'),
    path('auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('user/', CurrentUserView.as_view(), name='current-user'),
    path('profiles/<str:username>/', UserViewSet.as_view({
        'get': 'retrieve'
    }), name='profile-detail'),
    path('articles/<slug:slug>/comments/', CommentViewSet.as_view({
        'get': 'list',
        'post': 'create'
    }), name='article-comments-list'),
    path('articles/<slug:slug>/comments/<int:pk>/', CommentViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'patch': 'partial_update',
        'delete': 'destroy'
    }), name='article-comments-detail'),
]
