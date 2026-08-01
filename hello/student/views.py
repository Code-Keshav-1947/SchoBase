from functools import wraps
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from .models import Student
from teacher.models import Teacher
from .forms import StudentForm
from django.contrib.auth import get_user_model
from django.db import transactiont

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



User = get_user_model()  # Django ka custom/default user model fetch karne ka sahi tarika

from django.shortcuts import get_object_or_404, redirect, render
from django.db import transaction
from classes.models import Class
from section.models import Section

@login_required
@teacher_or_admin_required
def create_student(request):
    teacher = get_object_or_404(Teacher, user=request.user)
    school_obj = teacher.school
    teacher_class = teacher.class_teacher_of  # The Class object assigned to this teacher

    if request.method == 'POST':
        # Bind both form data and uploaded files (profile picture)
        form = StudentForm(request.POST, request.FILES, school=school_obj, teacher=teacher)
        
        if form.is_valid():
            stu_fir_name = form.cleaned_data.get('first_name')
            stu_las_name = form.cleaned_data.get('last_name')
            roll_no = form.cleaned_data.get('roll_no')
            
            user_name = f'{stu_fir_name}' # for testing purpose, you can change this to a more unique username generation logic
            temp_password = 'zxc mnbv'

            with transaction.atomic():
                # 1. Create the base custom user instance
                user_instance = User.objects.create_user(
                    username=user_name.lower(),
                    password=temp_password,
                    role='student',
                    first_name=stu_fir_name,
                    last_name=stu_las_name,
                )
                
                # 2. Extract and construct the Student model instance using commit=False
                student = form.save(commit=False)
                student.user = user_instance
                student.school = school_obj
                student.class_name = teacher_class
                student.save()
            messages.success(request, "Student created successfully!")   
            return redirect('student:student_list')
    else:
        # Pass school and teacher context down to filter querysets on initial load
        form = StudentForm(school=school_obj, teacher=teacher)
        
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