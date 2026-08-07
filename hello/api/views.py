from rest_framework import viewsets
from student.models import Student
from .serializers import StudentSerializer, TeacherSerializer
from teacher.models import Teacher

class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    
class TeacherViewSet(viewsets.ModelViewSet):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer
