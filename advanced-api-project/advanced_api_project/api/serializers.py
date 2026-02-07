from rest_framework import serializers
from .models import Book
from .models import Author
from django.utils import timezone


# Book serializer class
class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['title', 'publication_year', 'author']

    # Validate book publication year to not accept future dates
    def validate_publication_year(self, value):
        current_year = timezone.now().year

        if value > current_year:
            raise serializers.ValidationError('Publication year cannot be in the future')

        return value

# Author serializer class
class AuthorSerializer(serializers.ModelSerializer):

    # Nested books serializer to display books of each author
    books = BookSerializer(many=True, read_only=True)
    class Meta:
        model = Author
        fields = ['name', 'books']
