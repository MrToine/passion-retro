from django import forms

class CreateGuestbook(forms.Form):
    author = forms.CharField(
        max_length=150, 
        label='', 
        widget=forms.TextInput(attrs={'placeholder': 'Nom'})
    )
    content = forms.CharField(
        label='', 
        widget=forms.Textarea(attrs={'placeholder': 'Message'})
    )