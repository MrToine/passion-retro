from django import forms

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