from django.db import models
from school.models import School
from django.conf import settings

# Create your models here.
class Student(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    school = models.ForeignKey(School, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100, blank=True)
    admission_no = models.CharField(max_length=20, unique=True)
    roll_no = models.IntegerField()
    class_name = models.CharField(max_length=20)
    section = models.CharField(max_length=5)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=10)
    phone = models.CharField(max_length=15, blank=True)
    address = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
      return f"{self.first_name} - {self.roll_no} - {self.school}"
  