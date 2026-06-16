from django.contrib import admin
from django.contrib.auth.models import User
from .models import AccountProfile

@admin.register(AccountProfile)
class AccountProfileAdmin(admin.ModelAdmin):
    # Only display the fields that actually exist in your model
    list_display = ('id', 'user', 'phone_number', 'sex')
    search_fields = ('user__username', 'user__email')