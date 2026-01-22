from django.urls import path
from django.urls import include
from .views import list_books
from .views import LibraryDetailView
from .views import admin_view
from .views import librarian_view
from .views import member_view
from .views import add_book
from .views import edit_book
from .views import delete_book
from . import views
from django.contrib.auth.views import LoginView, LogoutView


urlpatterns = [
    path('list_books/', list_books, name='list_books'),
    path('library_detail/<int:pk>/', LibraryDetailView.as_view(), name='library_detail'),
    path('relationship_app/', include('django.contrib.auth.urls')),
    path('register/', views.register, name='register'),
    path('login/', LoginView.as_view(template_name='relationship_app/login.html'), name='login'),
    path('logout/', LogoutView.as_view(template_name='relationship_app/logout.html'), name='logout'),
    path('admin_view/', admin_view, name='admin_view'),
    path('librarian_view/', librarian_view, name='librarian_view'),
    path('member_view/', member_view, name='member_view'),
    path('add_book/', add_book, name='add_book'),
    path('edit_book/<int:pk>/', edit_book, name='edit_book'),
    path('delete_book/<int:pk>/', delete_book, name='delete_book'),
]