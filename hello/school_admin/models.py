from django.db import models
from school.models import School
from django.contrib.auth import get_user_model
# Create your models here.

User = get_user_model()

class Adminstrators(models.Model):
    name = models.CharField(max_length=100)
    school = models.ForeignKey(School,on_delete=models.CASCADE)
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name