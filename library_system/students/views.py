from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Student
from .forms import StudentRegistrationForm, StudentUpdateForm

def student_create_view(request):
    if request.method == 'POST':
        form = StudentRegistrationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            email = form.cleaned_data['email']

            # Create user login credentials in the background
            new_django_user = User.objects.create_user(
                username=username,
                email=email,
                password=password
            )

            # Create student profile record mapped via Foreign Key / OneToOne
            student_profile = form.save(commit=False)
            student_profile.user = new_django_user
            student_profile.save()

            messages.success(request, f'Member "{student_profile.name}" has been registered successfully.')
            return redirect('students:student_list')
        else:
            # Render form again with errors
            return render(request, 'students/student_form.html', {'form': form})

    # GET: show blank form
    form = StudentRegistrationForm()
    return render(request, 'students/student_form.html', {'form': form})

def student_list_view(request):
    # Render HTML template with full student objects for the UI
    students = Student.objects.all()
    return render(request, 'students/student_list.html', {'students': students})

def student_update_view(request, pk):
    student = get_object_or_404(Student, pk=pk)
    if request.method == 'POST':
        form = StudentUpdateForm(request.POST, instance=student)
        if form.is_valid():
            updated_student = form.save()
            
            # Also update the related User's email
            user = updated_student.user
            if user:
                user.email = updated_student.email
                user.save()
                
            messages.success(request, f'Member "{updated_student.name}" has been updated successfully.')
            return redirect('students:student_list')
    else:
        form = StudentUpdateForm(instance=student)
        
    return render(request, 'students/student_update.html', {'form': form, 'student': student})