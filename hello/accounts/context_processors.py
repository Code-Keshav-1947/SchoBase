from django.contrib.auth.models import AbstractUser
from notification.models import Notification


def nav_items(request):
    # 1. Return empty if user is anonymous
    if not request.user.is_authenticated:
        return {"nav_items": []}

    # 2. Query data dynamically on EVERY request for the current user
    unread_count = Notification.objects.filter(
        user=request.user
    ).count()

    # 3. Define the role items inside the function so variables resolve dynamically
    nav_items_by_role = {
        "student": [
            {"name": "Homework", "url": "/#"},
            {"name": "View Profile", "url": "/student"},
            {"name": f"Notification ({unread_count})", "url": "/notification/"},
        ],
        "teacher": [
            {"name": "Send Homework", "url": "/#"},
            {"name": "Attendance", "url": "/#"},
            {"name": "View Profile", "url": "/teacher"},
            {"name": f"Notification ({unread_count})", "url": "/notification/"},
        ],
        "school_admin": [
            {"name": "Manage Teachers", "url": "/#"},
            {"name": "Manage Students", "url": "/#"},
            {"name": "View Profile", "url": "/#"},
            {"name": f"Notification ({unread_count})", "url": "/notification/"},
        ],
    }

    # 4. Get user role and return items
    role = getattr(request.user, "role", None)
    return {"nav_items": nav_items_by_role.get(role, [])}
