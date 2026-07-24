from django.db import models
from school.models import School
from django.conf import settings

# Create your models here.
class Student(models.Model):
    classes = [
        ("1st","1st"),
        ("2nd","2nd"),
        ("3rd","3rd"),
        ("4th","4th"),
        ("5th","5th"),
        ("6th","6th"),
        ("7th","7th"),
        ("8th","8th"),
        ("9th","9th"),
        ("10th","10th"),
        ("11th","11th"),
        ("12th","12th"),
    ]
    gender_choices = [
        ("male", "Male"),
        ("female", "Female"),
        ("other", "Other"),
    ]
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    school = models.ForeignKey(School, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100, blank=True)
    admission_no = models.CharField(max_length=20)
    roll_no = models.IntegerField()
    class_name = models.CharField(max_length=20, choices=classes)
    section = models.ForeignKey("section.Section", on_delete=models.CASCADE)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=6, choices=gender_choices)
    phone = models.CharField(max_length=15, blank=True)
    address = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
      return f"{self.first_name} - {self.roll_no} - {self.school}"
  