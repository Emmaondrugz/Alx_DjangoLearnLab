from rest_framework import generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from .models import Book
from .serializers import BookSerializer

# Step 1: List all books (Public Read-Only)
class BookListView(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

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