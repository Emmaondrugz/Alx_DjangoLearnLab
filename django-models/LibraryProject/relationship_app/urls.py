from django.urls import path
from django.urls import include
from .views import list_books
from .views import LibraryDetailView
from .views import SignUpView


urlpatterns = [
    path('list_books/', list_books, name='list_books'),
    path('library_detail/<int:pk>/', LibraryDetailView.as_view(), name='library_detail'),
    path('relationship_app/', include('django.contrib.auth.urls')),
    path('register/', SignUpView.as_view(), name='register')
]