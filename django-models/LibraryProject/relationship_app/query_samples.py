#import all objects from models
from .models import *

# Query all books by specific author
books = Book.objects.filter(author='author_name')

# list all books in a library
library = Library.objects.get(name='')
all_books = library.books.all()

for book in all_books:
    print(book.title)

# Retrieve the libarian of a library
library = Library.objects.get(name='')
librarian = Librarian.objects.get(library=library)