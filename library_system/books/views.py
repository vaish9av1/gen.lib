from django.shortcuts import render
from accounts.decorators import librarian_only
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.utils.decorators import method_decorator
from accounts.decorators import librarian_only
from .models import Book

# Secure every single view using your custom librarian access decorator
@method_decorator(librarian_only, name='dispatch')
class BookListView(ListView):
    model = Book
    template_name = 'books/book_list.html'
    context_object_name = 'books'

@method_decorator(librarian_only, name='dispatch')
class BookCreateView(CreateView):
    model = Book
    fields = ['title', 'author', 'isbn', 'quantity', 'available_quantity', 'cover_image']
    template_name = 'books/book_form.html'
    success_url = reverse_lazy('books:book_list')

@method_decorator(librarian_only, name='dispatch')
class BookUpdateView(UpdateView):
    model = Book
    fields = ['title', 'author', 'isbn', 'quantity', 'available_quantity', 'cover_image']
    template_name = 'books/book_form.html'
    success_url = reverse_lazy('books:book_list')

class CustomerBookListView(ListView):
    model = Book
    template_name = 'books/customer_book_list.html'
    context_object_name = 'books'

@method_decorator(librarian_only, name='dispatch')
class BookDeleteView(DeleteView):
    model = Book
    template_name = 'books/book_confirm_delete.html'
    success_url = reverse_lazy('books:book_list')

@librarian_only
def book_create_view(request):
    # Only accessable if logged-in user has role == 'librarian'
    return render(request, 'books/book_form.html')