from django.urls import path
from . import views


urlpatterns = [
    path('all_books/', views.display_list_view, name='all_books'),
    path('library_details/', views.DisplayDetailsView.as_view(), name='library_details')
]