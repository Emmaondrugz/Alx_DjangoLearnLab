from rest_framework import viewsets, generics
from rest_framework import permissions
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .permissions import IsAuthorOrReadOnly
from .models import Post
from .models import Comment
from .serializers import PostSerializer
from .serializers import CommentSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework.filters import OrderingFilter
from .pagination import StandardResultsPagination

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


class FeedAPIView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Get the list of user the current user is following
        followed_users = request.user.following.all()

        # Filter post where the author is in the list
        posts = Post.objects.filter(author__in=followed_users).order_by('-created_at')

        # serialize the data
        serializer = PostSerializer(posts, many=True)

        return Response(serializer.data)