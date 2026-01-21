from django.urls import path
from .views import BookTemplateView

urlpatterns = [
    # We use .as_view() because it is a class based view
    path('my_books/', BookTemplateView.as_view(), name='book_list')
]