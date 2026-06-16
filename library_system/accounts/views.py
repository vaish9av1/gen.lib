import random
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
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

            user = authenticate(request, username=username, password=password)

            if user is not None:
                otp = str(random.randint(100000, 999999))
                
                # 1. SAVE BOTH TO THE SECURE DATABASE SESSION 
                request.session['pre_2fa_user_id'] = user.id
                request.session['active_otp_code'] = otp
                
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
                    print(f"SMTP Error encountered: {e}")
                    # fail_silently=False will cause a crash if your SMTP credentials are bad.
                    # If you want the site to keep moving forward even if Gmail blocks Render:
                    # error_message = "Email delivery failed. Please check backend configurations."
                
                return redirect('accounts:otp_verify')
            else:
                error_message = "Invalid username or password."

    return render(request, 'accounts/login.html', {'form': form, 'error': error_message})

def otp_verify_view(request):
    user_id = request.session.get('pre_2fa_user_id')
    cached_otp = request.session.get('active_otp_code') # Pull cleanly from session storage

    if not user_id or not cached_otp:
        return redirect('accounts:login')
        
    form = OTPVerifyForm(request.POST or None)
    error_message = None
    
    if request.method == 'POST':
        if form.is_valid():
            entered_otp = form.cleaned_data.get('otp')
            
            if cached_otp and str(entered_otp) == str(cached_otp):
                from django.contrib.auth.models import User
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