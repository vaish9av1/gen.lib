import random
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.core.cache import cache
from django.core.mail import send_mail
from django.conf import settings
from .forms import LoginForm, OTPVerifyForm

def login_view(request):
    form = LoginForm(request.POST or None)
    error_message = None

    if request.method == 'POST':
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            # Authenticate against Django's default User model
            user = authenticate(request, username=username, password=password)

            if user is not None:
                # User is valid. Generate OTP for 2FA.
                otp = str(random.randint(100000, 999999))
                
                # Store OTP in cache with 5 minute expiry
                cache_key = f"otp_2fa_{user.id}"
                cache.set(cache_key, otp, timeout=300)
                
                # Store user id in session temporarily to know who is logging in
                request.session['pre_2fa_user_id'] = user.id
                
                # Send email
                subject = "Your gen.lib Login OTP"
                message = f"Hello {user.username},\n\nYour OTP for logging into gen.lib is: {otp}\n\nThis OTP is valid for 5 minutes."
                try:
                    send_mail(
                        subject,
                        message,
                        settings.DEFAULT_FROM_EMAIL,
                        [user.email],
                        fail_silently=False,
                    )
                except Exception as e:
                    print(f"Error sending email: {e}")
                    # Even if email fails (e.g. SMTP not configured), the user should see the error 
                    # or we can log it. For now, we still redirect them.
                
                return redirect('accounts:otp_verify')
            else:
                error_message = "Invalid username or password."

    return render(request, 'accounts/login.html', {'form': form, 'error': error_message})

def otp_verify_view(request):
    user_id = request.session.get('pre_2fa_user_id')
    if not user_id:
        return redirect('accounts:login')
        
    form = OTPVerifyForm(request.POST or None)
    error_message = None
    
    if request.method == 'POST':
        if form.is_valid():
            entered_otp = form.cleaned_data.get('otp')
            cache_key = f"otp_2fa_{user_id}"
            cached_otp = cache.get(cache_key)
            
            if cached_otp and str(entered_otp) == str(cached_otp):
                # OTP is correct. Fetch user and log them in.
                from django.contrib.auth.models import User
                try:
                    user = User.objects.get(id=user_id)
                    login(request, user)
                    
                    # Clear session variable and cache
                    del request.session['pre_2fa_user_id']
                    cache.delete(cache_key)
                    
                    if user.is_staff:
                        return redirect('books:book_list')
                    else:
                        return redirect('home')
                except User.DoesNotExist:
                    error_message = "User not found."
            else:
                error_message = "Invalid or expired OTP."

    return render(request, 'accounts/otp_verify.html', {'form': form, 'error': error_message})

def logout_view(request):
    logout(request)
    return redirect('accounts:login')

from django.contrib import messages
from .forms import UserSignUpForm
from django.contrib.auth.models import User
from students.models import Student

def signup_view(request):
    form = UserSignUpForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            username = form.cleaned_data.get('username')
            name = form.cleaned_data.get('name')
            email = form.cleaned_data.get('email')
            phone = form.cleaned_data.get('phone')
            password = form.cleaned_data.get('password')

            # 1. Create Django Core User
            #    NOTE: The post_save signal in accounts/signals.py automatically
            #    creates a Student profile with placeholder data when a non-staff
            #    User is created. So we do NOT create a Student manually here.
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password
            )

            # 2. Update the auto-created Student profile with real form data
            #    (The signal already created it with placeholders)
            try:
                student = Student.objects.get(user=user)
                student.name = name
                student.email = email
                student.phone = phone
                student.save()
            except Student.DoesNotExist:
                # Fallback: create if signal didn't fire for some reason
                Student.objects.create(
                    user=user,
                    name=name,
                    email=email,
                    phone=phone
                )

            # 3. Log user in directly
            login(request, user)
            messages.success(request, f"Welcome to gen.lib, {name}! Your account has been registered successfully.")
            return redirect('home')

    return render(request, 'accounts/signup.html', {'form': form})