from django.urls import path, include
from .views import BookList, BookViewSet, BookListCreateView
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token

router = DefaultRouter()
router.register(r'books_all', BookViewSet, basename='book_all')

urlpatterns = [
    path('books/', BookListCreateView.as_view(), name='book-list'),
    path('', include(router.urls)),
    # The endpoint to get a token
    path('api-token-auth/', obtain_auth_token, name='api_token_auth')
]