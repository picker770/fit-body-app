from django import forms
from .models import ProgressPost


class ProgressPostForm(forms.ModelForm):
    class Meta:
        model = ProgressPost
        fields = ['title', 'caption', 'image']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'What did you achieve?'
            }), 
            'caption': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Share your progress story...'
            }),
            'image': forms.FileInput(attrs={
                'class': 'form-control',
            }),
        }