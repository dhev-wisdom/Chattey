from django import forms
from .models import ChatRoom

class GroupChatForm(forms.ModelForm):
    class Meta:
        model = ChatRoom
        fields = ['name', 'description', 'participants']