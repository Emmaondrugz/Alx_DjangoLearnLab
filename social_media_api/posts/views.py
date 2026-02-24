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
from rest_framework.generics import get_object_or_404

from ..notifications.models import Notification


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

    def Post(self, request, pk):
        # Get the specific post
        target_post = get_object_or_404(Post, pk)
        current_user = request.user

        # check if the user already liked this post (Avoid duplications)
        like_obj, created = Like.objects.get_or_create(user=current_user, post=target_post)

        if not created:
            return Response({'error: you already liked this post'}, status.HTTP_400_BAD_REQUEST)

        # Only notify if the liker is not the author
        if target_post.author != current_user:
            Notification.objects.create(
                recipient=target_post.author,
                actor=current_user,
                verb="liked",
                target=target_post,  # This maps to the GenericForeignKey
            )

        return Response('Post has been liked', status.HTTP_201_CREATED)

class UnlikePostView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        current_user = request.user
        target_post = get_object_or_404(Post, pk=pk)

        like_obj, created = Like.objects.get_or_create(user=current_user, post=target_post)

        if not created:
            like_obj.delete()
            return Response('Post has been unliked', status.HTTP_200_OK)
        else:
            if target_post.author != current_user:
                Notification.objects.create(
                    recipient=target_post.author,
                    actor=current_user,
                    verb="liked",
                    target=target_post,
                )
            return Response('Post has been liked', status.HTTP_201_CREATED)

