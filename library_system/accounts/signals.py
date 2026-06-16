from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from students.models import Student

@receiver(post_save, sender=User)
def create_student_profile(sender, instance, created, **kwargs):
    # If a brand-new user account is created and they aren't an admin/staff member...
    if created and not instance.is_staff:
        Student.objects.create(
            user=instance,
            name=instance.username,  # Fallback name
            email=instance.email,
            phone="Not Provided"     # Placeholder string
        )