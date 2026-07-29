from django.db import models
from school.models import School
from django.conf import settings
from django.db.models.signals import post_delete
from django.dispatch import receiver


# Create your models here.
class Student(models.Model):
    gender_choices = [
        ("male", "Male"),
        ("female", "Female"),
        ("other", "Other"),
    ]
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    school = models.ForeignKey(School, on_delete=models.CASCADE)
    profile_pic = models.ImageField(upload_to='profiles_pics/', blank=True, null=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100, blank=True)
    admission_no = models.CharField(max_length=20)
    roll_no = models.IntegerField()
    class_name = models.ForeignKey("classes.Class", on_delete=models.CASCADE)
    section = models.ForeignKey("section.Section", on_delete=models.CASCADE)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=6, choices=gender_choices)
    phone = models.CharField(max_length=15, blank=True)
    address = models.CharField(blank=True, null=True, help_text="Enter the address of the student",max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} - {self.roll_no} - {self.school}"


# Signal to delete the User account automatically when Student is deleted
@receiver(post_delete, sender=Student)
def delete_associated_user(sender, instance, **kwargs):
    if instance.user:
        instance.user.delete()
