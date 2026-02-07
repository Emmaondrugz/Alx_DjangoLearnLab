from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status

from advanced_features_and_security.LibraryProject.relationship_app.query_samples import author
from .models import Book

# Create your tests here.

class BookAPITestCase(APITestCase):
    def test_can_get_book_list(self):
        """Test that we can retrieve the list of books"""
        # Make a GET request to the endpoint
        response = self.client.get('/api/books/')

        # Check that the response is successfull
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # check if the data in the response is empty
        self.assertEqual(response.data, [])



