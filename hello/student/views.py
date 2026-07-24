from functools import wraps
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required


def teacher_or_admin_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if request.user.role not in ['teacher', 'school_admin']:
            return redirect('dashboard')
        return view_func(request, *args, **kwargs)
    return wrapper


@login_required
def index(request):
    return render(request, 'student/student_profile.html')

@login_required
@teacher_or_admin_required
def create(request):
    return render(request, 'student/create_student.html')

@login_required
@teacher_or_admin_required
def student_list(request):
    return render(request, 'student/list_students.html')

@login_required
@teacher_or_admin_required
def update(request, pk):
    return render(request, 'student/update_student.html', {'pk': pk})

@login_required
@teacher_or_admin_required
def delete(request, pk):
    return render(request, 'student/delete_student.html', {'pk': pk})