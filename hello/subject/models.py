from django.db import models


# Create your models here.
class Subject(models.Model):
    name = models.CharField(max_length=50)
    section = models.ForeignKey("section.Section", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} - {self.section.class_name.name}"
