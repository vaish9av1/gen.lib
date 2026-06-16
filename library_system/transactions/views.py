from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from datetime import timedelta
from books.models import Book
from students.models import Student
from .models import BookIssue

def issue_book_view(request, book_id, student_id):
    book = get_object_or_404(Book, id=book_id)
    student = get_object_or_404(Student, id=student_id)

    # Business Rule Safety Check: Is the book even available?
    if book.available_quantity > 0:
        # 1. Deduct 1 from the book's stock
        book.available_quantity -= 1
        book.save()

        # 2. Log the transaction entry in the database
        BookIssue.objects.create(
            student=student,
            book=book,
            transaction_type='issue',
            due_date=timezone.now() + timedelta(days=14) # Hardcoded 2-week return window
        )
        return redirect('transactions:transaction_list')
    else:
        # Handle error if book is out of stock
        return render(request, 'transactions/error.html', {'message': 'Book is currently out of stock.'})

def checkout_view(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    
    # Customer must be logged in to checkout
    if not request.user.is_authenticated or request.user.is_staff:
        # Redirect to login or show error
        return redirect('accounts:login')
        
    student = get_object_or_404(Student, user=request.user)

    if request.method == 'POST':
        if book.available_quantity > 0:
            book.available_quantity -= 1
            book.save()

            BookIssue.objects.create(
                student=student,
                book=book,
                transaction_type='issue',
                due_date=timezone.now() + timedelta(days=14)
            )
            return render(request, 'transactions/checkout_success.html', {'book': book})
        else:
            return render(request, 'transactions/error.html', {'message': 'Book is currently out of stock.'})

    return render(request, 'transactions/checkout.html', {'book': book, 'student': student})

from django.contrib import messages
from accounts.decorators import librarian_only

@librarian_only
def issue_list_view(request):
    issues = BookIssue.objects.all().order_by('-issue_date')
    return render(request, 'transactions/issue_list.html', {'issues': issues})

@librarian_only
def return_book_view(request, issue_id):
    issue = get_object_or_404(BookIssue, id=issue_id)
    if issue.status == 'Issued':
        issue.status = 'Returned'
        issue.return_date = timezone.now().date()
        issue.save()
        
        # Increase book's available quantity by 1
        book = issue.book
        book.available_quantity += 1
        book.save()
        messages.success(request, f'Book "{book.title}" returned successfully.')
    return redirect('transactions:issue_list')