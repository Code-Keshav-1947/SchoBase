from django.db import models

# Create your models here.
class Section(models.Model):
    school = models.ForeignKey("school.School", on_delete=models.CASCADE)
    class_name = models.ForeignKey("classes.Class", on_delete=models.CASCADE)
    name = models.CharField(max_length=5)
    def __str__(self):
        return f"{self.name} - {self.class_name.name}"