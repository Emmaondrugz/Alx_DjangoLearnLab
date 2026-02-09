from rest_framework import serializers
from .models import Book
from .models import Author
from django.utils import timezone

# Book serializer for the Book model
class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['title', 'publication_year', 'author']

    # Custom validation to prevent future date
    def validate_publication_year(self, data):
        present = timezone.now().year

        if data > present:
            raise serializers.ValidationError("can't use future dates.")

        return data

# Author serializer for the Author model
class AuthorSerializer(serializers.ModelSerializer):
    books = BookSerializer(many=True, read_only=True)

    class Meta:
        model = Author
        fields = ['name', 'books']

