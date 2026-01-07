# Update Operation
Command:
>>> book = Book.objects.get(title="1984")
>>> book.title = "Nineteen Eighty-Four"
>>> book.save()
>>> print(Book.objects.get(author="George Orwell").title)

Output:
Nineteen Eighty-Four