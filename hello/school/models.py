from django.db import models


# Create your models here.
class School(models.Model):
    boards = [
        ("CBSE", "CBSE"),
        ("ICSE", "ICSE"),
        ("State Board", "State Board"),
        ("IB", "IB"),
        ("OTHER", "OTHER"),
    ]
    school_name = models.TextField(max_length=50)
    school_board = models.CharField(max_length=20, choices=boards, default="CBSE")
    conatact_number = models.CharField(max_length=15, unique=True, null=True)
    email = models.EmailField(max_length=50, unique=True, null=True)
    address = models.CharField(max_length=100)
    joined_date = models.DateField(auto_now_add=True, null=True)

    def __str__(self):
        return self.school_name
