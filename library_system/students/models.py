from django.db import models
from django.contrib.auth.models import User # Import Django's default User table

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student_profile', null=True, blank=True)
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)

    def __str__(self):
        return self.name
    
    @property
    def is_borrower(self):
        if self.user:
            return not self.user.is_staff
        return True