import random
import resend
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.models import User
from students.models import Student
from .forms import LoginForm, OTPVerifyForm, UserSignUpForm

# Hardcode the API key directly as a string so it initializes instantly
resend.api_key = "re_6S88hkd3_AQUpJeWnQnC7K7RYRVCU9p7g"

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
                
                # ----------------------------------------------------------------
                # RESEND API DELIVERY (Bypasses Render's port restrictions completely)
                # ----------------------------------------------------------------
                try:
                    resend.Emails.send({
                        "from": "onboarding@resend.dev",
                        "to": user.email, # Make sure your user account has a real email address!
                        "subject": "Your gen.lib Login OTP",
                        "html": f"""
                            <div style="font-family: Arial, sans-serif; padding: 20px; border: 1px solid #eee; border-radius: 5px;">
                                <h2 style="color: #333;">Your gen.lib Security Code</h2>
                                <p>Hello <strong>{user.username}</strong>,</p>
                                <p>Your OTP for logging into the Library System is:</p>
                                <div style="font-size: 24px; font-weight: bold; padding: 10px 20px; background-color: #f4f4f4; display: inline-block; letter-spacing: 2px; color: #007bff; border-radius: 4px;">
                                    {otp}
                                </div>
                                <p style="color: #666; font-size: 12px; margin-top: 20px;">This OTP is valid for 5 minutes. If you did not request this code, please secure your account credentials.</p>
                            </div>
                        """
                    })
                except Exception as e:
                    print(f"Resend Send Error: {e}")
                # ----------------------------------------------------------------
                
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