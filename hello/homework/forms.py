from django import forms
from .models import Homework
class HomeworkForm(forms.models):
    class Meta:
        model = Homework
        fields = [
            'subject',
            'body',
            'date_submited_required'
        ]
        widgets = {
            'body':forms.Textarea(attrs={
                'rows':4,
                'placeholder':'Enter the assignment details...',
                'class':'form-control'
            }),
            'date_submited_required':forms.DateTimeInput(attrs={
                'type':'datetime-local',
                'class':'form-control'
            }),
            'subject': forms.Select(attrs={'class': 'form-control'})
        }