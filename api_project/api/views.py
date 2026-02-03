import rest_framework.generics
from django.shortcuts import render
from .models import Book
from .serializers import BookSerializer
import rest_framework.viewsets


# Create your views here.
class BookList(rest_framework.generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

class BookViewSet(rest_framework.viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer