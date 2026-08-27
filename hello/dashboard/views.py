from datetime import date
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from student.models import Student
from teacher.models import Teacher
from school_admin.models import Adminstrators
from classes.models import Class
from section.models import Section
from subject.models import Subject
from attendence.models import Attendance
from homework.models import Homework
from notification.models import Notification

# Create your views here.

@login_required
def dashboard(request):
    if request.user.is_staff == True:
        return redirect("/admin")
    user_role = getattr(request.user, "role", None)
    if request.user.role == "student" and request.user.is_active == True:
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
    if request.user.role == "teacher" and request.user.is_active == True:
        user_ = get_object_or_404(Teacher, user=request.user)
        user_name = user_.first_name
        has_marked_attendance = Attendance.objects.filter(marked_by=user_,date = date.today()).exists()
        fee_status = "Pending"
        if not has_marked_attendance:
            att_url = 'attendance/take_attendance'
            text = "Take attendance for your students"
            head = "Take Attendance"
        elif has_marked_attendance:
            head = "Preview Attendance"
            att_url = 'attendance/view'
            text = "Preview your students attendance"

        cards = [
            {
                "head": head,
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
                "url": 'homework/send/',
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
                "url": "",
            },
        ]
        return render(request, "dashboard/teacher_dashboard.html", {"cards": cards, "user_name": user_name})
    if request.user.role == "school_admin" and request.user.is_active == True:
        admin = get_object_or_404(Adminstrators, user=request.user)
        school = admin.school
        user_name = admin.name
        today = date.today()

        # Core Metrics
        total_students = Student.objects.filter(school=school).count()
        total_teachers = Teacher.objects.filter(school=school).count()
        total_classes = Class.objects.filter(school=school).count()
        total_sections = Section.objects.filter(school=school).count()
        total_subjects = Subject.objects.filter(section__school=school).distinct().count()
        total_homework = Homework.objects.filter(section__school=school).count()

        # Attendance Analytics
        today_attendance = Attendance.objects.filter(student__school=school, date=today)
        present_count = today_attendance.filter(status='P').count()
        absent_count = today_attendance.filter(status='A').count()
        leave_count = today_attendance.filter(status='L').count()
        total_marked = present_count + absent_count + leave_count
        pending_count = max(0, total_students - total_marked)
        att_rate = round((present_count / total_students * 100), 1) if total_students > 0 else 0.0

        attendance_analytics = {
            "date": today,
            "present": present_count,
            "absent": absent_count,
            "leave": leave_count,
            "pending": pending_count,
            "total_marked": total_marked,
            "rate": att_rate,
            "present_pct": round((present_count / total_students * 100), 1) if total_students > 0 else 0,
            "absent_pct": round((absent_count / total_students * 100), 1) if total_students > 0 else 0,
            "leave_pct": round((leave_count / total_students * 100), 1) if total_students > 0 else 0,
            "pending_pct": round((pending_count / total_students * 100), 1) if total_students > 0 else 100,
        }

        # Classes and Sections detailed roster breakdown
        classes_roster = []
        for cls in Class.objects.filter(school=school):
            sections = Section.objects.filter(class_name=cls).select_related('class_teacher')
            stu_count = Student.objects.filter(class_name=cls).count()
            classes_roster.append({
                "class": cls,
                "sections": sections,
                "student_count": stu_count,
            })

        # Recent activities & roster samples
        recent_students = (
            Student.objects.filter(school=school)
            .select_related('class_name', 'section')
            .order_by('-created_at')[:6]
        )
        teachers_list = (
            Teacher.objects.filter(school=school)
            .prefetch_related('class_teacher_of')[:6]
        )
        recent_notifications = (
            Notification.objects.filter(user=request.user)
            .order_by('-created_at')[:5]
        )

        stats = {
            "students": total_students,
            "teachers": total_teachers,
            "classes": total_classes,
            "sections": total_sections,
            "subjects": total_subjects,
            "homework": total_homework,
        }

        context = {
            "admin": admin,
            "school": school,
            "user_name": user_name,
            "stats": stats,
            "attendance": attendance_analytics,
            "classes_roster": classes_roster,
            "recent_students": recent_students,
            "teachers_list": teachers_list,
            "recent_notifications": recent_notifications,
            "today": today,
        }
        return render(request, "dashboard/school_admin.html", context)
    else:
        return redirect("/accounts/login/")

