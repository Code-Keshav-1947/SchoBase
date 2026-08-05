from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from classes.models import Class
from teacher.models import Teacher
from student.models import Student
from school.models import School
# Create your views here.
@login_required
def take_attendance(request):
    teacher = Teacher.objects.get(user=request.user)
    class_name = Class.objects.get(class_teacher_of=teacher)
    students = Student.objects.filter(class_name=class_name)
    return render(request, 'attendance/take_attendance.html', {'students': students})