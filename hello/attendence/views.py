from datetime import date
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Prefetch
from student.models import Student
from teacher.models import Teacher
from school_admin.models import Adminstrators
from .models import Attendance


@login_required
def take_attendance(request):
    current_date = date.today()
    teacher = get_object_or_404(Teacher, user=request.user)
    teacher_class_name = teacher.class_teacher_of.first()

    if not teacher_class_name:
        messages.error(request, "You are not assigned as a class teacher to any class.")
        return redirect('dashboard')

    students = Student.objects.filter(class_name=teacher_class_name).order_by('roll_no')

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

    context = {
        'students': students,
        'current_date': current_date,
        'class_name': teacher_class_name
    }
    return render(request, 'attendance/take_attendance.html', context)


@login_required 
def view_att(request):
    current_date = date.today()
    
    if request.user.role == 'school_admin':
        admin = get_object_or_404(Adminstrators, user=request.user)
        school = admin.school
        todays_attendance = Attendance.objects.filter(date=current_date, student__school=school)
        students = (
            Student.objects.filter(school=school)
            .select_related('class_name', 'section')
            .prefetch_related(
                Prefetch('attendance_set', queryset=todays_attendance, to_attr='today_attendance')
            )
            .order_by('class_name__name', 'roll_no')
        )
        class_label = f"All Classes ({school.school_name})"
    elif request.user.role == 'teacher':
        teacher = get_object_or_404(Teacher, user=request.user)
        teacher_class = teacher.class_teacher_of.first()
        
        if not teacher_class:
            messages.error(request, "You are not assigned as a class teacher to any class.")
            return redirect('dashboard')
        
        todays_attendance = Attendance.objects.filter(date=current_date)
        students = (
            Student.objects.filter(class_name=teacher_class)
            .prefetch_related(
                Prefetch('attendance_set', queryset=todays_attendance, to_attr='today_attendance')
            )
            .order_by('roll_no')
        )
        class_label = teacher_class.name
    else:
        return redirect('dashboard')
    
    for student in students:
        record = student.today_attendance[0] if student.today_attendance else None
        student.current_status = record.get_status_display() if record else "Not Marked"

    return render(request, 'attendance/view_attendance.html', {
        'date': current_date,
        'class_name': {'name': class_label},
        'students': students,
    })
