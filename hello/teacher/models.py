from django.db import models
from django.conf import settings

# Create your models here.
class Teacher(models.Model):
    first_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    class_teacher_of = models.ForeignKey("classes.Class",on_delete=models.CASCADE)
    school = models.ForeignKey("school.School", on_delete=models.CASCADE)
    def __str__(self):
      return f"{self.user} - {self.class_teacher_of} - {self.school}"