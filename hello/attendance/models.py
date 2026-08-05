from django.db import models
from student.models import Student
from classes.models import Class
# Create your models here.
class Attendance(models.Model):
    class StudentChoices(models.TextChoices):
        PRESENT = 'P', 'Present'
        ABSENT = 'A', 'Absent'
        LEAVE = 'L', 'Leave'
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    class_name = models.ForeignKey(Class, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    marked_by = models.CharField(max_length=50, blank=True, null=True)
    remarks = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=1, choices=StudentChoices.choices, default=StudentChoices.ABSENT)
    class Meta:
        unique_together = ('student','date')
    def __str__(self):
        return f"{self.student} - {self.class_name} - {self.date} - {self.status}"