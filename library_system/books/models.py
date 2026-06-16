from django.db import models

class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    isbn = models.CharField(max_length=13, unique=True)
    quantity = models.PositiveIntegerField()
    cover_image = models.ImageField(upload_to='book_covers/', null=True, blank=True)
    available_quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.title} by {self.author}"

    class Meta:
        unique_together = ('title', 'author')