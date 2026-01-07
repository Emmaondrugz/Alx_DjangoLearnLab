# Delete Operation
Command:
>>> book = Book.objects.get(title="The fall of olympus")
>>> book.delete()
>>> Book.objects.all()

Output:
(1, {'bookshelf.Book': 1})
<QuerySet []>