from django.urls import path
from . import views


urlpatterns = [
    path('list_books/', views.display_list_view, name='list_books'),
    path('library_detail/', views.DisplayDetailsView.as_view(), name='library_detail')
]