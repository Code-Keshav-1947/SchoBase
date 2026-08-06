from datetime import date  # Python ka safe and simple date module
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from classes.models import Class
from teacher.models import Teacher
from student.models import Student
from .models import Attendance 

@login_required
def take_attendance(request):
    try:
        teacher = Teacher.objects.get(user=request.user)
        class_name = Class.objects.get(class_teacher_of=teacher)
    except Teacher.DoesNotExist:
        return render(request, 'attendance/error.html', {'message': "Aap teacher account se logged in nahi hain."})
    except Class.DoesNotExist:
        return render(request, 'attendance/error.html', {'message': "Aapko abhi tak kisi bhi class ka Class Teacher nahi banaya gaya hai."})

    students = Student.objects.filter(class_name=class_name)
    
    # Timezone-safe standard date (Yeh error nahi dega)
    today = date.today()

    if request.method == "POST":
        for student in students:
            # HTML form se values uthana
            status_value = request.POST.get(f'status_{student.id}', 'P')
            
            # Database mein update ya insert karna
            Attendance.objects.update_or_create(
                student=student,
                date=today,
                defaults={
                    'classroom': class_name,
                    'status': status_value,
                    'marked_by': request.user
                }
            )
        
        messages.success(request, f"Class {class_name} ki attendance save ho gayi hai!")
        # Agar tumhare paas koi success dashboard page abhi nahi hai, toh wapas isi page par redirect kar do
        return redirect('take_attendance') 

    context = {
        'students': students,
        'class_name': class_name,
        'today': today
    }
    return render(request, 'attendance/take_attendance.html', context)
