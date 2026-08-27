from functools import wraps
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from .models import Student
from teacher.models import Teacher
from .forms import StudentForm
from django.contrib.auth import get_user_model
from django.conf import settings
from django.db import transaction
from section.models import Section
from notification.models import Notification
from school_admin.models import Adminstrators

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
    user_role = getattr(request.user, "role", None)
    if request.user.role == "student":
        # Pull related fields in one query (school, class, section) to avoid extra DB hits
        student = (
            Student.objects.select_related('school', 'class_name', 'section')
            .get(user=request.user)
        )
        return render(request, 'student/student_profile.html', {'student': student})
    else:
        return redirect('dashboard')



User = get_user_model()  # Django ka custom/default user model fetch karne ka sahi tarika


@login_required
@teacher_or_admin_required
def create_student(request):
    if request.user.role == 'teacher':
        teacher = get_object_or_404(Teacher, user=request.user)
        school_obj = teacher.school
    elif request.user.role == 'school_admin':
        admin_obj = get_object_or_404(Adminstrators, user=request.user)
        school_obj = admin_obj.school
        teacher = None
    else:
        return redirect('dashboard')

    if request.method == 'POST':
        form = StudentForm(request.POST, request.FILES, school=school_obj, teacher=teacher)
        
        if form.is_valid():
            stu_fir_name = form.cleaned_data.get('first_name', '').strip()
            stu_las_name = form.cleaned_data.get('last_name', '').strip()
            roll_no = form.cleaned_data.get('roll_no')
            admission_no = form.cleaned_data.get('admission_no', '').strip()
            
            # Generate a unique username based on admission_no or first_name + roll_no
            base_username = admission_no if admission_no else f"{stu_fir_name}_{roll_no}".lower()
            username = base_username.replace(' ', '_').lower()
            temp_password = f"{stu_fir_name.lower()}@123" if stu_fir_name else "scho1234"

            with transaction.atomic():
                # Avoid duplicate user collision
                if User.objects.filter(username=username).exists():
                    username = f"{username}_{roll_no}"

                user_instance = User.objects.create_user(
                    username=username,
                    password=temp_password,
                    role='student',
                    first_name=stu_fir_name,
                    last_name=stu_las_name,
                )
                
                student = form.save(commit=False)
                student.user = user_instance
                student.school = school_obj
                student.class_name = student.section.class_name
                student.save()
                
                form.save_m2m()
                
            Notification.objects.create(
                user=user_instance,
                message=f'Welcome to SchoBase! Your student account at {school_obj.school_name} has been created.'
            )   
            messages.success(request, f"Student '{stu_fir_name} {stu_las_name}' enrolled successfully!")   
            return redirect('student:student_list')
    else:
        form = StudentForm(school=school_obj, teacher=teacher)
        
    return render(request, 'student/create_student.html', {'form': form})

@login_required
@teacher_or_admin_required
def student_list(request):
    if request.user.role == 'teacher':
        teacher = get_object_or_404(Teacher, user=request.user)
        students = (
            Student.objects.filter(class_name__in=teacher.class_teacher_of.all())
            .select_related('class_name', 'school', 'section')
        )
    elif request.user.role == 'school_admin':
        admin_obj = get_object_or_404(Adminstrators, user=request.user)
        students = (
            Student.objects.filter(school=admin_obj.school)
            .select_related('class_name', 'school', 'section')
            .order_by('class_name__name', 'roll_no')
        )
    else:
        return redirect('dashboard')
    return render(request, 'student/list_student.html', {'students': students})


@login_required
@teacher_or_admin_required
def update_student(request, pk):
    if request.user.role == 'teacher':
        teacher = get_object_or_404(Teacher, user=request.user)
        school_obj = teacher.school
    elif request.user.role == 'school_admin':
        admin_obj = get_object_or_404(Adminstrators, user=request.user)
        school_obj = admin_obj.school
        teacher = None
    else:
        return redirect('dashboard')
        
    student = get_object_or_404(Student, pk=pk, school=school_obj)
    if request.method == 'POST':
        form = StudentForm(request.POST, request.FILES, instance=student, school=school_obj, teacher=teacher)
        if form.is_valid():
            updated_student = form.save(commit=False)
            updated_student.class_name = updated_student.section.class_name
            updated_student.save()
            form.save_m2m()
            messages.success(request, "Student details updated successfully!")
            return redirect('student:student_list')
    else:
        form = StudentForm(instance=student, school=school_obj, teacher=teacher)
    return render(request, 'student/update_student.html', {'form': form, 'student': student})


@login_required
@teacher_or_admin_required
def delete_student(request, pk):
    student = get_object_or_404(Student, pk=pk)
    if request.method == 'POST':
        student.delete()
        messages.success(request, "Student deleted successfully!")
        return redirect('student:student_list')
    return render(request, 'student/delete_student.html', {'student': student})