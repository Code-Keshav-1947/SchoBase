# yourapp/context_processors.py

NAV_ITEMS_BY_ROLE = {
    "student": [
        {"name": "Homework", "url": "/#"},
        {"name": "View Profile", "url": "/student"},
        {"name": "Notification", "url": "/#"},
    ],
    "teacher": [
        {"name": "Send Homework", "url": "/#"},
        {"name": "Attendance", "url": "/#"},
    ],
    "school_admin": [
        {"name": "Manage Teachers", "url": "/#"},
        {"name": "Manage Students", "url": "/#"},
    ],
}


def nav_items(request):
    if not request.user.is_authenticated:
        return {"nav_items": []}

    role = getattr(request.user, "role", None)
    return {"nav_items": NAV_ITEMS_BY_ROLE.get(role, [])}