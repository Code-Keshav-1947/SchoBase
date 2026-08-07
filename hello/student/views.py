from functools import wraps
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from .models import Student
from teacher.models import Teacher
from .forms import StudentForm
from django.contrib.auth import get_user_model
from django.db import transaction
from section.models import Section
from notification.models import Notification

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


@login_required
@teacher_or_admin_required
def create_student(request):
    teacher = get_object_or_404(Teacher, user=request.user)
    school_obj = teacher.school
    
    # FIX: Since class_teacher_of is a Many-to-Many relation, 
    # we must explicitly grab a specific class instance (e.g., the first one).
    teacher_class = teacher.class_teacher_of.first()  # <-- CHANGED THIS LINE

    if request.method == 'POST':
        form = StudentForm(request.POST, request.FILES, school=school_obj, teacher=teacher)
        
        if form.is_valid():
            stu_fir_name = form.cleaned_data.get('first_name')
            stu_las_name = form.cleaned_data.get('last_name')
            roll_no = form.cleaned_data.get('roll_no')
            
            # Appended roll_no to prevent IntegrityErrors with duplicate names
            user_name = f'{stu_fir_name}' 
            temp_password = 'zxc mnbv'

            with transaction.atomic():
                user_instance = User.objects.create_user(
                    username=user_name.lower(),
                    password=temp_password,
                    role='student',
                    first_name=stu_fir_name,
                    last_name=stu_las_name,
                )
                
                student = form.save(commit=False)
                student.user = user_instance
                student.school = school_obj
                student.class_name = teacher_class  # Assigned the single class object here
                student.save()
                
                form.save_m2m()  # Safe execution of form M2M data
            Notification.objects.create(
                user = user_instance,
                message = 'You are successfully created as an Student!'
            )   
            messages.success(request, "Student created successfully!")   
            return redirect('student:student_list')
    else:
        form = StudentForm(school=school_obj, teacher=teacher)
        
    return render(request, 'student/create_student.html', {'form': form})

@login_required
@teacher_or_admin_required
def student_list(request):
    if request.user.role == 'teacher':
        teacher = get_object_or_404(Teacher, user=request.user)
        # CHANGED: Added __in and .all() to handle the Many-to-Many field
        students = Student.objects.filter(class_name__in=teacher.class_teacher_of.all())
    else:
        students = Student.objects.all()

    return render(request, 'student/list_student.html', {'students': students})


@login_required
@teacher_or_admin_required
def update_student(request, pk):
    teacher = get_object_or_404(Teacher, user=request.user)
    school_obj = teacher.school
    teacher_class = teacher.class_teacher_of
    student = get_object_or_404(Student, pk=pk)
    if request.method == 'POST':
        form = StudentForm(request.POST, request.FILES, school=school_obj, teacher=teacher)
        if form.is_valid():
            student.first_name = form.cleaned_data['first_name']
            student.last_name = form.cleaned_data['last_name']
            student.admission_no = form.cleaned_data['admission_no']
            student.roll_no = form.cleaned_data['roll_no']
            student.section = form.cleaned_data['section']
            student.gender = form.cleaned_data['gender']
            profile_pic = form.cleaned_data.get('profile_pic')
            if profile_pic:
                student.profile_pic = profile_pic
        section = get_object_or_404(Section, pk=request.POST.get('section'))
        student.save()
        messages.success(request, "Student updated successfully!")  # Optional: Add a success message
        return redirect('student:student_list')
    return render(request, 'student/update_student.html', {'form': StudentForm(instance=student, school=school_obj, teacher=teacher), 'student': student})


@login_required
@teacher_or_admin_required
def delete_student(request, pk):
    student = get_object_or_404(Student, pk=pk)
    if request.method == 'POST':
        student.delete()
        messages.success(request, "Student deleted successfully!")  # Optional: Add a success message
        return redirect('student:student_list')
    return render(request, 'student/delete_student.html', {'student': student})