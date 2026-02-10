from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Book, Author
from django.contrib.auth.models import User


class TestBookAPI(APITestCase):

    def setUp(self):
        # 1. Create a User for Authentication
        self.user = User.objects.create_user(username='testuser', password='password123')

        # 2. Create an Author instance
        self.author = Author.objects.create(name='Emma')

        # 3. Create initial Book instances
        self.book1 = Book.objects.create(
            title='The fallen',
            author=self.author,
            publication_year=2026,
        )
        self.book2 = Book.objects.create(
            title='One Piece',
            author=self.author,
            publication_year=2022,
        )

        # Define URLs (Assuming your names in urls.py are 'book-list' and 'book-detail')
        self.list_url = reverse('book-list')
        self.detail_url = reverse('book-detail', kwargs={'pk': self.book1.id})

    # --- CRUD TESTS ---

    def test_create_book(self):
        """Test if a logged-in user can create a book"""
        self.client.login(username='testuser', password='password123')
        data = {
            "title": "New Horizons",
            "author": self.author.id,
            "publication_year": 2024
        }
        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 3)

    def test_get_all_books(self):
        """Test retrieving the list of books"""
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Check if both books created in setUp are present
        self.assertEqual(len(response.data), 2)

    def test_update_book(self):
        """Test updating a book's title"""
        self.client.login(username='testuser', password='password123')
        updated_data = {"title": "The Fallen: Revised", "author": self.author.id, "publication_year": 2026}
        response = self.client.put(self.detail_url, updated_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book1.refresh_from_db()
        self.assertEqual(self.book1.title, "The Fallen: Revised")

    def test_delete_book(self):
        """Test deleting a book"""
        self.client.login(username='testuser', password='password123')
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Book.objects.count(), 1)

    # --- FILTERING & SEARCH TESTS ---

    def test_filter_books_by_title(self):
        """Test filtering books by title query parameter"""
        response = self.client.get(f"{self.list_url}?title=One Piece")
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'One Piece')

    # --- PERMISSION TESTS ---

    def test_unauthenticated_cannot_create(self):
        """Ensure anonymous users cannot post data"""
        self.client.logout()
        data = {"title": "Ghost Book", "author": self.author.id, "publication_year": 2025}
        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)