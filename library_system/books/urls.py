from django.urls import path
from .views import BookListView, BookCreateView, BookUpdateView, BookDeleteView, CustomerBookListView

app_name = 'books'

urlpatterns = [
    path('', BookListView.as_view(), name='book_list'),
    path('browse/', CustomerBookListView.as_view(), name='book_browse'),
    path('add/', BookCreateView.as_view(), name='book_add'),
    path('edit/<int:pk>/', BookUpdateView.as_view(), name='book_edit'),
    path('delete/<int:pk>/', BookDeleteView.as_view(), name='book_delete'),
]