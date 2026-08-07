from rest_framework import serializers
from teacher.models import Teacher
from student.models import Student

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = "__all__"   # or list specific fields: ['id', 'name', 'age']

class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = "__all__"   # or list specific fields: ['id', 'name', 'subject']
