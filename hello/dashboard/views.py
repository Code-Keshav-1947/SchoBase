from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from student.models import Student
from teacher.models import Teacher
from attendence.models import Attendance
from datetime import date
# Create your views here.


@login_required
def dashboard(request):
    if request.user.role == "student":
        student_prof = get_object_or_404(Student, user=request.user)
        user_name = student_prof.first_name
        
        # Define status mapping dictionary
        status_mapping = {'A': 'Absent', 'P': 'Present','L':'Leave'}
        
        # Use filter().first() to avoid a 404 error if attendance isn't logged yet
        attendance = Attendance.objects.filter(student=student_prof, date=date.today()).first()
        att_status = status_mapping.get(attendance.status, 'Not Marked') if attendance else 'Not Marked'
            
        fee_status = "Pending"
        cards = [
            {
                "head": "Attendance",
                "text": "Your today Attendance status was",
                "status": att_status,
                "url": "/",
            },
            {
                "head": "Fees Status",
                "text": "Your Fees status was",
                "status": fee_status,
                "url": "#",
            },
        ]
        return render(request, "dashboard/student_dashboard.html", {"cards": cards, "user_name": user_name})
    elif request.user.role == "teacher":
        user_ = get_object_or_404(Teacher, user=request.user)
        user_name = user_.first_name
        att_status = Attendance.objects.filter(marked_by = user_)
        fee_status = "Pending"
        if not att_status:
            att_url = 'attendance/take_attendance'
            text = "Take attendance for your students"
        else:
            att_url = 'attendance/view'
            text = "Preview your students attendance"

        cards = [
            {
                "head": "Take Attendance",
                "text": text,
                "status": '',
                "url": att_url,
            },
            {
                "head": "View Students",
                "text": "View students in your class and their details and edit them",
                "status": "",
                "url": "student/list_students/",
            },
            {
                "head": "Send Homework",
                "text": "Send homework to your students",
                "status": "",
                "url": "#",
            },
            {
                "head":"Add Students",
                "text":"Add the Students",
                "status":"",
                "url":"/student/create_student/"
            },
            {
                "head": "Fees Status",
                "text": "Preview your students fees status",
                "status": "",
                "url": "#",
            },
        ]
        return render(request, "dashboard/teacher_dashboard.html", {"cards": cards, "user_name": user_name})
    elif request.user.role == "school_admin":
        return render(request, "dashboard/school_admin.html")
    elif request.user.is_staff == True:
        return redirect("/admin")
    else:
        return redirect( login_required)
