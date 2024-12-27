from django import forms
from .models import Post

class CreatePost(forms.Form):
    title = forms.CharField(
        max_length=150, 
        label='', 
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'Titre du post'})
    )

    content = forms.CharField(
        label='', 
        required=True,
        widget=forms.Textarea(attrs={'placeholder': 'Contenu du post'})
    )

    active = forms.BooleanField(
        required=True, 
        label='Actif',
        initial=True
    )

class EditPost(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Titre du post'}),
            'content': forms.Textarea(attrs={'placeholder': 'Contenu du post'}),
        }