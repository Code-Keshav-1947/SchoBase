from django.shortcuts import get_object_or_404, redirect, render
from teacher.models import Teacher
from school_admin.models import Adminstrators

# Create your views here.
def teacher_profile(request):
    if request.user.role == 'teacher':
        teacher = get_object_or_404(Teacher, user=request.user)
        return render(request, 'teacher/teacher_profile.html', {'teacher': teacher})
    else:
        return redirect('dashboard')

        
def list_teachers(request):
    if request.user.role == 'school_admin':
        admin = get_object_or_404(Adminstrators, user=request.user)
        school = admin.school
        teachers = Teacher.objects.filter(school=school)
        return render(request, 'teacher/teacher_list.html', {'teachers': teachers})
    else:
        return redirect('dashboard')