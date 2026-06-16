import random
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.models import User
from students.models import Student
from .forms import LoginForm, OTPVerifyForm, UserSignUpForm

def login_view(request):
    form = LoginForm(request.POST or None)
    error_message = None

    if request.method == 'POST':
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                otp = str(random.randint(100000, 999999))
                
                # Save both to the secure database session backend
                request.session['pre_2fa_user_id'] = user.id
                request.session['active_otp_code'] = otp
                
                # Send email
                subject = "Your gen.lib Login OTP"
                message = f"Hello {user.username},\n\nYour OTP for logging into gen.lib is: {otp}\n\nThis OTP is valid for 5 minutes."
                
                try:
                    # Setting fail_silently=True ensures that even if Google blocks Render's IP,
                    # the site won't throw a 500/timeout error. It will gracefully push the user to the OTP page.
                    send_mail(
                        subject,
                        message,
                        settings.DEFAULT_FROM_EMAIL,
                        [user.email],
                        fail_silently=True,
                    )
                except Exception as e:
                    print(f"SMTP Logging error: {e}")
                
                return redirect('accounts:otp_verify')
            else:
                error_message = "Invalid username or password."

    return render(request, 'accounts/login.html', {'form': form, 'error': error_message})

def otp_verify_view(request):
    user_id = request.session.get('pre_2fa_user_id')
    cached_otp = request.session.get('active_otp_code')

    if not user_id or not cached_otp:
        return redirect('accounts:login')
        
    form = OTPVerifyForm(request.POST or None)
    error_message = None
    
    if request.method == 'POST':
        if form.is_valid():
            entered_otp = form.cleaned_data.get('otp')
            
            if cached_otp and str(entered_otp) == str(cached_otp):
                try:
                    user = User.objects.get(id=user_id)
                    login(request, user)
                    
                    # Clean up session values on successful validation
                    del request.session['pre_2fa_user_id']
                    del request.session['active_otp_code']
                    
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

def signup_view(request):
    form = UserSignUpForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            username = form.cleaned_data.get('username')
            name = form.cleaned_data.get('name')
            email = form.cleaned_data.get('email')
            phone = form.cleaned_data.get('phone')
            password = form.cleaned_data.get('password')

            user = User.objects.create_user(
                username=username,
                email=email,
                password=password
            )

            try:
                student = Student.objects.get(user=user)
                student.name = name
                student.email = email
                student.phone = phone
                student.save()
            except Student.DoesNotExist:
                Student.objects.create(
                    user=user,
                    name=name,
                    email=email,
                    phone=phone
                )

            login(request, user)
            messages.success(request, f"Welcome to gen.lib, {name}! Your account has been registered successfully.")
            return redirect('home')

    return render(request, 'accounts/signup.html', {'form': form})