from django import forms
from django.contrib.auth.models import User  
from .models import Student
from accounts.models import AccountProfile  

class StudentRegistrationForm(forms.ModelForm):
    # Standard login fields for Django's built-in User table
    username = forms.CharField(
        max_length=150, 
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Pick a unique username'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'})
    )
    
    # Optional fields from your custom AccountProfile table
    phone_number = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Optional: Alternate phone'})
    )
    sex = forms.ChoiceField(
        choices=[('', 'Select Gender'), ('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')],
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Student
        fields = ['name', 'email', 'phone']  # Fields going directly to the Student table
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Student\'s Full Name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'example@college.com'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Primary Student Phone'}),
        }

    # === ADD THESE VALIDATION METHODS BELOW TO PREVENT DUPLICATE ERRORS ===

    def clean_username(self):
        """Checks if the chosen username is already taken in the User table."""
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("This username is already taken. Please pick another one.")
        return username

    def clean_email(self):
        """Checks if the email is already registered in either the Student or User table."""
        email = self.cleaned_data.get('email')
        
        # 1. Check if a student record uses this email
        if Student.objects.filter(email=email).exists():
            raise forms.ValidationError("A library student profile with this email address already exists.")
            
        # 2. Check if a core Django user login profile uses this email
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email address is already linked to an active user account.")
            
        return email

class StudentUpdateForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['name', 'email', 'phone']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Student\'s Full Name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'example@college.com'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Primary Student Phone'}),
        }
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        
        # Check if email is used by another student
        if Student.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError("A library student profile with this email address already exists.")
            
        # Check if email is used by another user
        if User.objects.filter(email=email).exclude(pk=self.instance.user.pk).exists():
            raise forms.ValidationError("This email address is already linked to another user account.")
            
        return email