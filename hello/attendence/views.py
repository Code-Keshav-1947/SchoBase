from datetime import date
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from student.models import Student
from teacher.models import Teacher
from .models import Attendance


@login_required
def take_attendance(request):
    current_date = date.today()
    teacher = get_object_or_404(Teacher, user=request.user)
    teacher_class_name = teacher.class_teacher_of.first()

    # Prevent errors if the teacher is not assigned to any class
    if not teacher_class_name:
        messages.error(request, "You are not assigned as a class teacher to any class.")
        return redirect('dashboard')

    students = Student.objects.filter(class_name=teacher_class_name)

    if request.method == 'POST':
        for student in students:
            status_value = request.POST.get(f'status_{student.id}')
            if status_value:
                Attendance.objects.update_or_create(
                    student=student,
                    date=current_date,
                    defaults={
                        'marked_by': teacher,
                        'status': status_value
                    }
                )
        messages.success(request, "Attendance saved successfully!")
        return redirect('dashboard')

    # Fixed: Context must be a dictionary
    context = {
        'students': students,
        'current_date': current_date,
        'class_name': teacher_class_name
    }
    return render(request, 'attendance/take_attendance.html', context)
