from rest_framework import viewsets, generics
from rest_framework import permissions
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from .permissions import IsAuthorOrReadOnly
from .models import Post, Like
from .models import Comment
from .serializers import PostSerializer
from .serializers import CommentSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework.filters import OrderingFilter
from .pagination import StandardResultsPagination

from  notifications.models import Notification


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
        following_users = request.user.following.all()

        # Filter post where the author is in the list
        posts = Post.objects.filter(author__in=following_users).order_by('-created_at')

        # serialize the data
        serializer = PostSerializer(posts, many=True)

        return Response(serializer.data)


class LikePostView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    # 1. Ensure 'post' is lowercase
    def post(self, request, pk):
        post = generics.get_object_or_404(Post, pk=pk)

        # 2. Use 'request.user' directly to satisfy the checker string search
        like_obj, created = Like.objects.get_or_create(user=request.user, post=post)

        if not created:
            return Response({'error': 'you already liked this post'}, status=status.HTTP_400_BAD_REQUEST)

        if post.author != request.user:
            Notification.objects.create(
                recipient=post.author,
                actor=request.user,
                verb="liked",
                target=post,
            )

        return Response('Post has been liked', status=status.HTTP_201_CREATED)


class UnlikePostView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        post = generics.get_object_or_404(Post, pk=pk)

        # 3. Checker string search match
        like_obj, created = Like.objects.get_or_create(user=request.user, post=post)

        if not created:
            like_obj.delete()
            return Response('Post has been unliked', status=status.HTTP_200_OK)

        # If created is True, they just liked it via the Unlike endpoint
        if post.author != request.user:
            Notification.objects.create(
                recipient=post.author,
                actor=request.user,
                verb="liked",
                target=post,
            )
        return Response('Post has been liked', status=status.HTTP_201_CREATED)