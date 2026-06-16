from django.db import models
from books.models import Book
from students.models import Student

class BookIssue(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    issue_date = models.DateField(auto_now_add=True)
    return_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=50, default='Issued')
    due_date = models.DateField(null=True, blank=True)
    transaction_type = models.CharField(max_length=50, default='Issued')
    
    def __str__(self):
        return f"{self.book.title} - {self.student.name}"