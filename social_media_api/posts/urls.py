from django.urls import path
from django.urls import include
from rest_framework.routers import DefaultRouter

from social_media_api.posts.views import CommentViewSet
from views import PostViewSet

router = DefaultRouter()
router.register(r'posts/', PostViewSet)
router.register(r'comments', CommentViewSet)

urlpatterns = [
    path('', include(router.urls)),
]