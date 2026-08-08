from django.db import models

class Attendance(models.Model):
    # 1. Inherit from models.TextChoices
    class Status(models.TextChoices):
        PRESENT = 'P', 'Present'
        ABSENT = 'A', 'Absent'
        LEAVE = 'L', 'Leave'
        PENDING = 'Pen', 'Pending'

    # 2. Changed to ForeignKey so a student can have multiple daily records
    student = models.ForeignKey(
        "student.Student", 
        verbose_name="Student", 
        on_delete=models.CASCADE
    )
    marked_by = models.ForeignKey(
        "teacher.Teacher",  
        on_delete=models.CASCADE
    )
    date = models.DateField()
    
    # 3. Added max_length (longest database value is 'Pen', which is 3 characters)
    status = models.CharField(
        max_length=3,
        choices=Status.choices,  # Use .choices for explicit safety
        default=Status.PENDING
    )

    class Meta:
        # 4. Modern way to ensure one attendance record per student per day
        constraints = [
            models.UniqueConstraint(
                fields=['student', 'date'], 
                name='unique_student_attendance_per_day'
            )
        ]
