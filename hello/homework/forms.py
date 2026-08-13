from django import forms
from .models import Homework
from subject.models import Subject

class HomeworkForm(forms.ModelForm): # Fixed forms.models to forms.ModelForm
    class Meta:
        model = Homework
        fields = [
            'subject',
            'body',
            'date_submitted_required'
        ]
        widgets = {
            'body': forms.Textarea(attrs={
                'rows': 4,
                'placeholder': 'Enter the assignment details...',
                'class': 'form-control'
            }),
            'date_submitted_required':forms.DateTimeInput(
                format='%Y-%m-%dT%H:%M',
                attrs={'type': 'datetime-local', 'class': 'form-control'}
            ),
            'subject': forms.Select(attrs={'class': 'form-control'})
        }
    def __init__(self,*args, **kwargs):
        section = kwargs.pop('section',None)
        super().__init__(*args, **kwargs)
        
        self.fields['subject'].empty_label = 'Select Subject'
        
        if section:
            # Filter the queryset for the foreign key field
            self.fields['subject'].queryset = Subject.objects.filter(section=section)