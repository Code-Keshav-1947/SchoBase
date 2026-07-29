from functools import wraps
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from .models import Student
from teacher.models import Teacher
from .forms import StudentForm

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
    if request.method == 'POST':
        form = StudentForm(request.POST, request.FILES)
        if form.is_valid():
            student = form.save(commit=False)
            # Assign the user to the student if needed
            # student.user = some_user_instance
            student.save()
            return redirect('student:student_list')
    else:
        form = StudentForm()
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