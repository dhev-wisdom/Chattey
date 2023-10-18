from django import forms
from .models import Message

class EditMessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['body']