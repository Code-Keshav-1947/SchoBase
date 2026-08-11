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

from django.db.models import Prefetch

def view_att(request):
    current_date = date.today()
    teacher = get_object_or_404(Teacher, user=request.user)
    teacher_class = teacher.class_teacher_of.first()
    
    # 1. Prefetch only today's attendance for efficiency
    todays_attendance = Attendance.objects.filter(date=current_date)
    
    # 2. Get students and automatically attach their attendance record for today
    students = Student.objects.filter(
        class_name=teacher_class
    ).prefetch_related(
        Prefetch('attendance_set', queryset=todays_attendance, to_attr='today_attendance')
    )
    
    # 3. Format data so the template can easily access the status
    for student in students:
        # Accesses the cached 'today_attendance' list created by Prefetch
        record = student.today_attendance[0] if student.today_attendance else None
        student.current_status = record.get_status_display() if record else "Not Marked"

    return render(request, 'attendance/view_attendance.html', {
        'date': current_date,
        'class_name': teacher_class,
        'students': students,
    })

