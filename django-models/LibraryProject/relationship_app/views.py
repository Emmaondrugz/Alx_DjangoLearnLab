from django.shortcuts import render
from .models import *
from django.views.generic import *

# Create your views here.
def display_list_view(request):
    books = Book.objects.all()
    context = {'all_books': books}
    return render(request, 'relationship_app/all_books.html', context)

class DisplayDetailsView(DetailView):
    model = Library
    template_name = 'relationship_app/library_details.html'
    context_object_name = 'library'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['books'] = self.objects.books.all()
        return context


















