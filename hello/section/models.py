from django.db import models
from teacher.models import Teacher  
from school import models as school_models
from classes import models as class_models  

# Create your models here.
class Section(models.Model):
    school = models.ForeignKey("school.School", on_delete=models.CASCADE, null=True, blank=True)
    class_name = models.ForeignKey("classes.Class", on_delete=models.CASCADE, null=True, blank=True)
    class_teacher = models.ForeignKey("teacher.Teacher", on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=5, null=True, blank=True)

    def __str__(self):
        return f"{self.class_name.name} - {self.name} - {self.school.school_name}"
