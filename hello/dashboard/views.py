from django.shortcuts import render, redirect

# Create your views here.
from django.contrib.auth.decorators import login_required


@login_required
def dashboard(request):
    if request.user.role == "student":
        att_status = "Pending..."
        fee_status = "Pending"
        cards = [
            {
                "head": "Attendance",
                "text": "Your today Attendance status was",
                "status": att_status,
                "url": "#",
            },
            {
                "head": "Fees Status",
                "text": "Your Fees status was",
                "status": fee_status,
                "url": "#",
            },
        ]
        return render(request, "dashboard/student_dashboard.html", {"cards": cards})
    elif request.user.role == "teacher":
        return render(request, "dashboard/teacher_dashboard.html")
    elif request.user.role == "school_admin":
      return render(request, "dashboard/school_admin.html")
    elif request.user.is_staff == True:
        return redirect("/admin")
    else:
      return redirect(request,'404.html')
        
