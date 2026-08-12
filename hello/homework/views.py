from django.shortcuts import render, redirect, get_object_or_404
from .forms import HomeworkForm
from teacher.models import Teacher
from section.models import Section
from django.contrib.auth.decorators import login_required
from django.utils import timezone  

@login_required
def ViewHomework(request):
    return render(request, 'homework/view_homework.html')

@login_required
def sendHomework(request):
    teacher_prof = get_object_or_404(Teacher, user=request.user)
    section = get_object_or_404(Section, class_teacher=teacher_prof)
    
    if request.method == 'POST':
        form = HomeworkForm(request.POST, request.FILES, section=section) # Form validation me bhi section pass karna safe hota hai
        if form.is_valid():
            form_ = form.save(commit=False) # Temporary object bana
            
            # Behind the scenes values set kiye
            form_.assigned_by = teacher_prof
            form_.date_assigned = timezone.now() # Sahi tarika timezone handle karne ka
            
            # CRITICAL FIX: Ise likhna zaroori hai taaki database me save ho!
            form_.save() 
            
            return redirect('view homework')
        else:   
            print("Form Errors:", form.errors)
    else:
        form = HomeworkForm(section=section)
        
    return render(request, 'homework/send_homework.html', {'form': form})
