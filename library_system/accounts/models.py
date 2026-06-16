from django.db import models
from django.contrib.auth.models import User 

class AccountProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    sex = models.CharField(
        choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')], 
        max_length=10, 
        blank=True, 
        null=True
    )

    def __str__(self):
        return f"Profile for {self.user.username}"