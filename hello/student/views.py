from functools import wraps
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from .models import Student
from teacher.models import Teacher
from .forms import StudentForm
from django.contrib.auth import get_user_model

user = get_user_model()

def teacher_or_admin_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if request.user.role not in ['teacher', 'school_admin']:
            return redirect('dashboard')
        return view_func(request, *args, **kwargs)
    return wrapper


@login_required
def index(request):
    if request.user.role == 'student':
        student = get_object_or_404(Student, user=request.user)
        return render(request, 'student/student_profile.html', {'student': student})
    else:
        return redirect('dashboard')

@login_required
@teacher_or_admin_required
def create_student(request):
    teacher_school = request.user.school if hasattr(request.user, 'school') else None

    if request.method == 'POST':
        form = StudentForm(request.POST, request.FILES, school=teacher_school)
        
        if form.is_valid():
            with transaction.atomic():
                # 1. Grab the unique admission number from the form to use as the username
                username = form.cleaned_data['first_name'] + form.cleaned_data['admission_no']
                
                # 2. Automatically create the User instance in the background
                user_instance = user.objects.create_user(
                    username=username,
                    password=f"Stud@{username}{form.cleaned_data['admission_no']}", # Auto password (e.g., Stud@ADM123)
                    role='student',
                    first_name=form.cleaned_data['first_name'],
                    last_name=form.cleaned_data['last_name']
                )
                
                # 3. Create the student record without committing to DB yet
                student = form.save(commit=False)
                
                # 4. Link the new User account to this student
                student.user = user_instance
                if teacher_school:
                    student.school = teacher_school
                
                # 5. Save the final student record completely
                student.save()
                
            return redirect('student:student_list')
    else:
        form = StudentForm(school=teacher_school)
    return render(request, 'student/create_student.html', {'form': form})

@login_required
@teacher_or_admin_required
def student_list(request):
    # filter for a specifc class which teacher is teaching or for a specific school if the user is a school admin
    if request.user.role == 'teacher':
        teacher = get_object_or_404(Teacher, user=request.user)
        students = Student.objects.filter(class_name=teacher.class_teacher_of)
    else:
        students = Student.objects.all()

    return render(request, 'student/list_student.html', {'students': students})

@login_required
@teacher_or_admin_required
def update_student(request, pk):
    student = get_object_or_404(Student, pk=pk)
    if request.method == 'POST':
        student.first_name = request.POST.get('first_name')
        student.last_name = request.POST.get('last_name')
        student.admission_no = request.POST.get('admission_no')  # Added to match your HTML form
        student.roll_no = request.POST.get('roll_no')            # Added to match your HTML form
        
        # REMOVED: student.class_name = request.POST.get('class_name') 
        # This line was overwriting your Foreign Key object with None
        
        student.save()
        return redirect('student:student_list')
    return render(request, 'student/update_student.html', {'student': student})


@login_required
@teacher_or_admin_required
def delete_student(request, pk):
    student = get_object_or_404(Student, pk=pk)
    if request.method == 'POST':
        student.delete()
        return redirect('student:student_list')
    return render(request, 'student/delete_student.html', {'student': student})