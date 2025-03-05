from django import forms
from .models import Request, Attachment

class Step1Form(forms.ModelForm):
    class Meta:
        model = Request
        fields = ['type']

class Step2Form(forms.ModelForm):
    class Meta:
        model = Request
        fields = ['title', 'description', 'priority']

class Step3Form(forms.ModelForm):
    class Meta:
        model = Request
        fields = ['deadline', 'additional_notes']

class AttachmentForm(forms.ModelForm):
    class Meta:
        model = Attachment
        fields = ['file']
