from rest_framework.permissions import BasePermission


# Custom permission classes
class IsTeacher(BasePermission):
    """Allow access only to users with role='teacher'."""

    def has_permission(self, request, view):
        return bool(
            request.user
            and request.user.is_authenticated
            and getattr(request.user, "role", None) == "teacher"
        )


class IsStudent(BasePermission):
    """Allow access only to users with role='student'."""

    def has_permission(self, request, view):
        return bool(
            request.user
            and request.user.is_authenticated
            and getattr(request.user, "role", None) == "student"
        )


class IsSchoolAdmin(BasePermission):
    """Allow access only to users with role='school_admin'."""

    def has_permission(self, request, view):
        return bool(
            request.user
            and request.user.is_authenticated
            and getattr(request.user, "role", None) == "school_admin"
        )
