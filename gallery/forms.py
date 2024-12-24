from django import forms

class AddImgGallery(forms.Form):
    image = forms.FileField(
        label='Image',
        required=True,
        widget=forms.ClearableFileInput(attrs={'class': 'form-inline'})
    )

    def clean_img(self):
        img = self.cleaned_data.get('image')
        if img:
            if not img.name.lower().endswith(('.jpg', '.jpeg', '.png')):
                raise forms.ValidationError('Seul les fichiers JPG, JPEG, PNG sont autorisés.')
            if img.size > 5 * 1024 * 1024:
                raise forms.ValidationError('La taille de l\'image ne dois pas dépasser 5 Mo.')
        return img