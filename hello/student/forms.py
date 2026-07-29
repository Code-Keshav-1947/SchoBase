from django import forms
from .models import Student

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        # List all the fields you want to show in the HTML form
        fields = [
            'first_name', 
            'last_name', 
            'school',        # ForeignKey -> Renders as Dropdown
            'class_name',    # ForeignKey -> Renders as Dropdown
            'section',       # ForeignKey -> Renders as Dropdown
            'date_of_birth', 
            'gender', 
            'phone', 
            'address', 
            'profile_pic'
        ]
        
        # Optional: Add Bootstrap classes to style the dropdowns and inputs
        widgets = {
            'school': forms.Select(attrs={'class': 'form-control'}),
            'class_name': forms.Select(attrs={'class': 'form-control'}),
            'section': forms.Select(attrs={'class': 'form-control'}),
            'date_of_birth': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }