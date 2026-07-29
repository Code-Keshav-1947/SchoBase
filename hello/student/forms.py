# student/forms.py
from django import forms
from .models import Student
from classes.models import Class  
from section.models import Section

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        # Exclude 'user' and do not add any 'email' fields here
        fields = [
            'admission_no',  # Added this so we can use it for the username
            'roll_no',
            'first_name', 
            'last_name', 
            'school',        
            'class_name',    
            'section',       
            'date_of_birth', 
            'gender', 
            'phone', 
            'address', 
            'profile_pic'
        ]
        
        widgets = {
            'admission_no': forms.TextInput(attrs={'class': 'form-control'}),
            'roll_no': forms.NumberInput(attrs={'class': 'form-control'}),
            'school': forms.Select(attrs={'class': 'form-control'}),
            'class_name': forms.Select(attrs={'class': 'form-control'}),
            'section': forms.Select(attrs={'class': 'form-control'}),
            'date_of_birth': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'gender': forms.Select(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        school = kwargs.pop('school', None)
        super().__init__(*args, **kwargs)
        
        if school:
            self.fields['class_name'].queryset = Class.objects.filter(school=school)
            self.fields['section'].queryset = Section.objects.filter(class_name__school=school)
            self.fields['school'].initial = school
            self.fields['school'].disabled = True