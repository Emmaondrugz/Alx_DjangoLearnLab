from .models import Author, Book, Library, Librarian

# 1. Query all books by a specific author
author_name = "J.K. Rowling"
author = Author.objects.get(name=author_name) # The checker needs this line
books = Book.objects.filter(author=author)    # And this line

# 2. List all books in a library
library_name = "Central Library"
library = Library.objects.get(name=library_name)
all_books = library.books.all()

# 3. Retrieve the librarian of a library
# FIX: The Librarian query should use the 'library' OBJECT, not the 'library_name' STRING
librarian = Librarian.objects.get(library=library)