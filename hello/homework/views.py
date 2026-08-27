from django.shortcuts import render, redirect, get_object_or_404
from .forms import HomeworkForm
from teacher.models import Teacher
from student.models import Student
from section.models import Section
from django.contrib.auth.decorators import login_required
from django.utils import timezone  
from .models import Homework
from school_admin.models import Adminstrators

@login_required
def ViewHomework(request):
    if request.user.role == 'student':
        student = get_object_or_404(Student,user= request.user)
        section = student.section
        homework = Homework.objects.filter(section=section)
        return render(request, 'homework/view_homework.html',{'homework':homework })
    if request.user.role == "teacher":
        homework = Homework.objects.filter(assigned_by=request.user.teacher)
        return render(request,'homework/view_homework.html',{'homework':homework })
    if request.user.role == "school_admin":
        school = get_object_or_404(Adminstrators,user=request.user).school
        sections = Section.objects.filter(school=school)
        homework = Homework.objects.filter(section__in=sections)
        return render(request,'homework/view_homework.html',{'homework':homework })

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
            form_.date_assigned = timezone.now() 
            form_.section = section
            form_.save() 
            
            return redirect('view homework')
        else:   
            print("Form Errors:", form.errors)
    else:
        form = HomeworkForm(section=section)
        
    return render(request, 'homework/send_homework.html', {'form': form})
