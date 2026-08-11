from django import forms
from .models import Student
from section.models import Section

# 1. Base Form containing all configurations and filtering logic
class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = [
            'first_name', 'last_name', 'profile_pic', 'admission_no', 
            'roll_no', 'section', 'gender', 'date_of_birth', 'phone', 'address'
        ]
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'profile_pic': forms.FileInput(attrs={'class': 'form-control'}),
            'admission_no': forms.TextInput(attrs={'class': 'form-control'}),
            'roll_no': forms.NumberInput(attrs={'class': 'form-control'}),
            'section': forms.Select(attrs={'class': 'form-control'}),
            'gender': forms.Select(attrs={'class': 'form-control'}),
            'date_of_birth': forms.DateInput(attrs={'type': 'date', 'class': 'form-control custom-date'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }

    def __init__(self, *args, **kwargs):
        # Pop custom parameters before calling super()
        school = kwargs.pop('school', None)
        teacher = kwargs.pop('teacher', None)
        super().__init__(*args, **kwargs)
        
        # FIX: Check if the teacher has any assigned classes using .exists()
        if teacher and teacher.class_teacher_of.exists():
            # FIX: Use __in because class_teacher_of is a Many-to-Many field
            self.fields['section'].queryset = Section.objects.filter(
                class_name__in=teacher.class_teacher_of.all()
            ).order_by('name')
        else:
            self.fields['section'].queryset = Section.objects.none()


# 2. Update Form inherits directly from StudentForm
# No duplicate code needed; it automatically keeps fields, widgets, and filtering!
class StudentUpdateForm(StudentForm):
    pass
