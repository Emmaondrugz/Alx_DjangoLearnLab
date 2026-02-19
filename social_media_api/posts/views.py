from rest_framework import viewsets
from rest_framework import permissions
from .permissions import IsAuthorOrReadOnly
from .models import Post
from .models import Comment
from .serializers import PostSerializer
from .serializers import CommentSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework.filters import OrderingFilter
from pagination import StandardResultsPagination

# Create your views here.
class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated, IsAuthorOrReadOnly]
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    search_fields = ['title', 'content']
    ordering_fields = ['created_at']
    Pagination_class = [StandardResultsPagination]


    def perform_create(self, serializer):
        # Automatically attach the logged-in user as the user
        serializer.save(author=self.request.user)

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated, IsAuthorOrReadOnly]
    pagination_class = [StandardResultsPagination]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)