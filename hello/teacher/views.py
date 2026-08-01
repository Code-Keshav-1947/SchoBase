from django.shortcuts import get_object_or_404, redirect, render
from teacher.models import Teacher

# Create your views here.
def teacher_profile(request):
    if request.user.role == 'teacher':
        teacher = get_object_or_404(Teacher, user=request.user)
        return render(request, 'teacher/teacher_profile.html', {'teacher': teacher})
    else:
        return redirect('dashboard')