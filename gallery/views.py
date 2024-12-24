from django.shortcuts import render
from django.contrib import messages
from .forms import AddImgGallery
from django.contrib.auth.decorators import login_required
import os
from django.conf import settings

@login_required()
def home(request):
    user_id = request.user.id
    user_directory = os.path.join(settings.MEDIA_ROOT, 'galleries', str(user_id))
    img_urls = []

    if os.path.exists(user_directory):
        for filename in os.listdir(user_directory):
            if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
                img_urls.append(f"{settings.MEDIA_URL}galleries/{user_id}/{filename}")

    return render(request, 'gallery/home.html', {'images': img_urls})

@login_required()
def import_img(request):
    if request.method == "POST":
        form = AddImgGallery(request.POST, request.FILES)
        if form.is_valid():
            image = form.clean_img()
            user_id = request.user.id 
            saved_image_url = save_image_to_gallery(image, user_id)

            messages.success(request, 'Votre image a bien été ajoutée à la galerie')
    form = AddImgGallery()
    return render(request, 'gallery/form.html', {'form': form})

def save_image_to_gallery(image, user_id):
    user_directory = os.path.join(settings.MEDIA_ROOT, 'galleries', str(user_id))
    os.makedirs(user_directory, exist_ok=True) 
    
    # Créer un fichier index.html vide pour sécuriser le répertoire
    index_file_path = os.path.join(user_directory, 'index.html')
    if not os.path.exists(index_file_path):  # Vérifie si le fichier n'existe pas déjà
        with open(index_file_path, 'w') as index_file:
            index_file.write('')  # Écrit un fichier vide
    
    # Définir le chemin complet du fichier
    file_path = os.path.join(user_directory, image.name)

    # Enregistrer le fichier
    with open(file_path, 'wb+') as destination:
        for chunk in image.chunks():
            destination.write(chunk)

    return f"{settings.MEDIA_URL}galleries/{user_id}/{image.name}" 