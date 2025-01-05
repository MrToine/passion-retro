from django import forms
from .models import *

# Gestion des formulaires pour les quiz en se servant du model
class QuizForm(forms.ModelForm):
    class Meta:
        model = Quiz
        fields = ['name', 'description', 'image']
        labels = {
            'name': '',
            'description': '',
            'image': '(Pas obligatoire) '
        }
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Nom du quiz'}),
            'description': forms.Textarea(attrs={'placeholder': 'Un text de description pour que les membres aient une idée du contenu du quiz'}),
        }

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['question']

class ChoiceForm(forms.ModelForm):
    class Meta:
        model = Choice
        fields = ['choice', 'is_correct']