from django.shortcuts import render

# Create your views here.
def teacher_profile(request):
    return render(request, 'teacher/teacher_profile.html')