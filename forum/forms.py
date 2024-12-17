from django import forms

class CreateTopic(forms.Form):
    TOPIC_TYPE_CHOICES = (
        ('normal', 'Normal'),
        ('announce', 'Annonce'),
    )
    title = forms.CharField(
        max_length=150, 
        label='', 
        widget=forms.TextInput(attrs={'placeholder': 'Titre du sujet'})
    )
    content = forms.CharField(
        label='', 
        widget=forms.Textarea(attrs={'placeholder': 'Contenu du sujet'})
    )
    type = forms.ChoiceField(choices=TOPIC_TYPE_CHOICES, label='Type de sujet')

class CreatePost(forms.Form):
    content = forms.CharField(
        label='', 
        widget=forms.Textarea(attrs={'placeholder': 'Contenu du message'})
    )