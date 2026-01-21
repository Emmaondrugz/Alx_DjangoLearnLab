from django.shortcuts import render
from .models import Book
from django.views.generic import DetailView, TemplateView, ListView, CreateView
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.http import HttpResponse

# Create your views here.
def book_list_view(request):
    books = Book.objects.all()
    context = {'books_data': books}
    return render(request, 'books.html', context)

class BookListView(ListView):
    model = Book
    template_name = 'book.html'
    context_object_name = 'books'

class BookTemplateView(TemplateView):
    template_name = 'books.html'

class BookCreateView(CreateView):
    model = Book
    fields = ['author', 'title', 'publication_year']
    template_name = 'book/add_book.html'
    success_url = 'book/my_books.html'

    def form_invalid(self, form):
        messages.error(self.request, 'Something went wrong, please try again later.')
        return super().form_invalid(form)

class SignUpView(CreateView):
    form_class = UserCreationForm
    success_url = '/books.html'
    template_name = 'registration/sign_up.html'

