# Forms pour la messagerie
from django import forms
from .models import PrivateMessageSubject, PrivateMessage

class PrivateMessageSubjectForm(forms.ModelForm):
    class Meta:
        model = PrivateMessageSubject
        fields = ['receiver', 'subject']
        labels = {
            'receiver': 'Destinataire',
            'subject': 'Sujet'
        }

class PrivateMessageForm(forms.ModelForm):
    class Meta:
        model = PrivateMessage
        fields = ['message']
        labels = {
            'message': ''
        }
        widgets = {
            'message': forms.Textarea(attrs={'placeholder': 'Votre message'})
        }