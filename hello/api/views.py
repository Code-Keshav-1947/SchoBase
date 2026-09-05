from rest_framework import viewsets

# import the models
from student.models import Student
from teacher.models import Teacher
from school.models import School
from notification.models import Notification
from classes.models import Class
from section.models import Section
from attendence.models import Attendance

# imports the serializers
from .serializers import (
    StudentSerializer,
    TeacherSerializer,
    SchoolSerializer,
    NotificationSerializer,
    ClassSerializer,
    SectionSerializer,
    AttendanceSerializer,
)
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .permissions import IsTeacher, IsStudent, IsSchoolAdmin


class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Return all students if the user is an admin or school_admin, otherwise return only their own students
        if self.request.user.is_superuser or self.request.user.role == "school_admin":
            return Student.objects.all()
        return Student.objects.filter(user=self.request.user)

    def get_permissions(self):
        if self.action in ["list", "retrieve"]:
            return [IsAuthenticated()]
        return [IsAuthenticated(), IsSchoolAdmin()]


class TeacherViewSet(viewsets.ModelViewSet):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Return all teachers if the user is an admin or school_admin, otherwise return only their own teachers
        if self.request.user.is_superuser or self.request.user.role == "school_admin":
            return Teacher.objects.all()
        return Teacher.objects.filter(user=self.request.user)


class SchoolViewSet(viewsets.ModelViewSet):
    queryset = School.objects.all()
    serializer_class = SchoolSerializer


class ClassViewSet(viewsets.ModelViewSet):
    queryset = Class.objects.all()
    serializer_class = ClassSerializer


class SectionViewSet(viewsets.ModelViewSet):
    queryset = Section.objects.all()
    serializer_class = SectionSerializer


class NotificationViewSet(viewsets.ModelViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer


class AttendanceViewSet(viewsets.ModelViewSet):
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer
