from rest_framework import generics
from rest_framework.permissions import AllowAny,IsAuthenticatedOrReadOnly, IsAuthenticated
from .models import Book
from .serializers import BookSerializer
from django_filters import rest_framework

# Step 1: List all books (Public Read-Only)
from rest_framework import generics, filters
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .models import Book
from .serializers import BookSerializer


class BookListView(generics.ListAPIView):
    serializer_class = BookSerializer
    permission_classes = [AllowAny]

    # 1. Define Filter Backends as Class Attributes
    # This enables built-in Search and Ordering alongside your custom filtering
    filter_backends = [rest_framework, filters.SearchFilter, filters.OrderingFilter]

    # Configuration for built-in SearchFilter
    search_fields = ['title', 'author', 'publication_year']

    # Configuration for built-in OrderingFilter
    ordering_fields = ['title','author', 'publication_year']

    def get_queryset(self):
        """
        Custom filtering logic to stack filters based on query parameters.
        """
        # Start with all objects
        queryset = Book.objects.all()

        # Get parameters from the URL
        title = self.request.query_params.get('title')
        author = self.request.query_params.get('author')
        publication_year = self.request.query_params.get('publication_year')

        # 2. Stack the filters (Use 'queryset = queryset.filter' to keep previous filters)
        if title:
            queryset = queryset.filter(title__icontains=title)
        if author:
            queryset = queryset.filter(author__icontains=author)
        if publication_year:
            # Note: icontains on an IntegerField works in some DBs but 'exact' is safer for years
            queryset = queryset.filter(publication_year=publication_year)

        return queryset

# Step 1: Retrieve single book (Public Read-Only)
class BookDetailView(generics.RetrieveAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

# Step 1 & 3: Create a book (Authenticated Only)
class BookCreateView(generics.CreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated] # Step 4 requirement

    # Step 3: Customization hook
    def perform_create(self, serializer):
        # Example: Logic to handle data before saving
        serializer.save()

# Step 1 & 3: Update a book (Authenticated Only)
class BookUpdateView(generics.UpdateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]

    # Step 3: Customization hook
    def perform_update(self, serializer):
        # Example: logic to log updates or modify data
        serializer.save()

# Step 1: Delete a book (Authenticated Only)
class BookDeleteView(generics.DestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]