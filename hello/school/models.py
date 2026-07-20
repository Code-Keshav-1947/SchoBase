from django.db import models

# Create your models here.
class School(models.Model):
  school_name = models.TextField(max_length=50)
  address = models.CharField(max_length=100)
  def __str__(self):
    return self.school_name
  
  