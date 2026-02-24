from django.urls import path
from django.urls import include
from rest_framework.routers import DefaultRouter

from .views import CommentViewSet, FeedAPIView
from .views import PostViewSet
from .views import UnlikePostView
from .views import LikePostView

router = DefaultRouter()
router.register(r'posts/', PostViewSet)
router.register(r'comments', CommentViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('feed/', FeedAPIView.as_view()),
    path('posts/<int:pk>/unlike/', UnlikePostView.as_view()),
    path('posts/<int:pk>/like/', LikePostView.as_view())
]