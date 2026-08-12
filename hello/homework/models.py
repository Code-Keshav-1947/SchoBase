from django.db import models

class Homework(models.Model):
    body = models.CharField(max_length=600)
    date_assigned = models.DateTimeField()
    subject = models.ForeignKey('subject.Subject', on_delete=models.CASCADE)
    date_submitted_required = models.DateTimeField()
    # Changed the relation string format
    assigned_by = models.ForeignKey('teacher.Teacher', on_delete=models.CASCADE)
    def __str__(self):
        return f"{self.subject} Homework (Assigned by: {self.assigned_by})"
