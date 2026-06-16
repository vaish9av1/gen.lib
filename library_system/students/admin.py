from django.contrib import admin
from .models import Student

class StudentAdmin(admin.ModelAdmin):
    # This pulls columns into your admin directory grid
    list_display = ('name', 'email', 'phone', 'get_username', 'get_is_staff')
    
    # This adds the sidebar filter to isolate non-staff (students)
    list_filter = ('user__is_staff',)

    def get_username(self, obj):
        return obj.user.username if obj.user else "No Account Assigned"
    get_username.short_description = 'Username'

    def get_is_staff(self, obj):
        if obj.user:
            return obj.user.is_staff
        return False
    get_is_staff.short_description = 'Is Staff?'
    get_is_staff.boolean = True # Gives you pretty checkmarks/X marks

admin.site.register(Student, StudentAdmin)