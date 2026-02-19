from rest_framework import serializers
from ..accounts.serializers import UserSerializer
from .models import Post
from .models import Comment

class PostSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')

    class Meta:
        model = Post
        fields = ('author', 'title', 'content', 'created_at', 'updated_at')

class CommentSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='author.username')

    class Meta:
        model = Comment
        field = ('post', 'user', 'content', 'created_at', 'updated_at')
