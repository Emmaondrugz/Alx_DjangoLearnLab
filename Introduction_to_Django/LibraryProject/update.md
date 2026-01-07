# Update Operation
Command:
>>> book = Book.objects.get(title="The fall")
>>> book.title = "The fall of olympus"
>>> book.save()
>>> print(Book.objects.get(author="Ekwere").title)

Output:
The fall of olympus