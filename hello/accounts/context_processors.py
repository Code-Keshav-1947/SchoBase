NAV_ITEMS_BY_ROLE = {
    "student": [
        {"name": "Homework", "url": "/homework"},
        {"name": "View Profile", "url": "/student"},
        {"name": "Notification", "url": "/notification"},
    ],
    "teacher": [
        {"name": "Send Homework", "url": "/homework/send"},
        {"name": "Attendance", "url": "/attendance/take_attendance"},
        {"name": "View Profile", "url": "/teacher"},
        {"name": "Notification", "url": "/notification"},
    ],
    "school_admin": [
        {"name": "Manage Teachers", "url": "/#"},
        {"name": "Manage Students", "url": "/#"},
        {"name": "View Profile", "url": "/#"},
        {"name": "Notification", "url": "/#"},
    ],
}


def nav_items(request):
    if not request.user.is_authenticated:
        return {"nav_items": []}

    role = getattr(request.user, "role", None)
    return {"nav_items": NAV_ITEMS_BY_ROLE.get(role, [])}
