from django import forms

from .models import User

class UserRegistrationForm(forms.Form):
    username = forms.CharField(
        label='', 
        max_length=150,
        widget=forms.TextInput(attrs={'class': 'form-group', 'placeholder': 'Pseudo'})
    )
    email = forms.EmailField(
        label='',
        widget=forms.EmailInput(attrs={'class': 'form-group', 'placeholder': 'Email'})
    )
    password1 = forms.CharField(
        label='',
        widget=forms.PasswordInput(attrs={'class': 'form-group', 'placeholder': 'Mot de passe'})
    )
    password2 = forms.CharField(
        label='',
        widget=forms.PasswordInput(attrs={'class': 'form-group', 'placeholder': 'Mot de passe (vérification)'})
    )

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords do not match")

class UserLoginForm(forms.Form):
    username = forms.CharField(
        label='', 
        max_length=150,
        widget=forms.TextInput(attrs={'class': 'form-group', 'placeholder': 'Pseudo'})
    )
    password = forms.CharField(
        label='',
        widget=forms.PasswordInput(attrs={'class': 'form-group', 'placeholder': 'Mot de passe'})
    )

class UserUpdateForm(forms.ModelForm):
    theme = forms.CharField(
        # On créer une liste de choix pour le thème
        label='Thème',
        widget=forms.Select(choices=[('default', 'Thème par defaut'), ('80s', 'Thème années 80'), ('00s', 'Thème années 2000')]),
    )
    class Meta:
        model = User
        fields = ['avatar', 'email', 'biography', 'theme']

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['avatar', 'biography']

class CompleteProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['avatar', 'birth_date', 'biography']

class PostForm(forms.Form):
    title = forms.CharField(
        max_length=150, 
        label='', 
        widget=forms.TextInput(attrs={'placeholder': 'Titre de l\'article'})
    )
    content = forms.CharField(
        label='', 
        widget=forms.Textarea(attrs={'placeholder': 'Contenu de l\'article'})
    )
