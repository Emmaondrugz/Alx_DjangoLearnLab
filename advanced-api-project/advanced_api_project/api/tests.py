from django.test import TestCase
from .models import Book, Author


class BookTestCase(TestCase):
    """Implement Book creation test"""

    def setUp(self):
        # Create Author first
        self.author = Author.objects.create(name='Oda')

        # Create Book with the author instance
        self.book = Book.objects.create(
            title='one piece',
            publication_year=2026,
            author=self.author  # Pass the Author object, not a string
        )

    def test_book_creation_works(self):  # ✅ Lowercase 'test_'
        # Get the book
        one_piece = Book.objects.get(title='one piece')

        # Test individual fields
        self.assertEqual(one_piece.title, 'one piece')
        self.assertEqual(one_piece.publication_year, 2026)
        self.assertEqual(one_piece.author.name, 'Oda')  # Access author's name