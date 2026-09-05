from django.db import models


# Create your models here.
class Class(models.Model):
    school = models.ForeignKey("school.School", on_delete=models.CASCADE)
    name = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.name } - {self.school}"
