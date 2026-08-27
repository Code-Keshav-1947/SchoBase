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
    phone = models.CharField(max_length=100, blank=True)
    address = models.CharField(max_length=255, blank=True)
    class_teacher_of = models.ManyToManyField("classes.Class", blank=True, related_name="class_teacher_of")
    school = models.ForeignKey("school.School", on_delete=models.CASCADE)

    def __str__(self):
        # 1. Fetch all assigned classes and join them with commas
        classes_list = ", ".join([str(cls) for cls in self.class_teacher_of.all()])
        
        # 2. Handle a fallback string if no classes are assigned yet
        classes_str = classes_list if classes_list else "No Classes Assigned"
        
        return f"{self.user} - ({classes_str}) - {self.school}"