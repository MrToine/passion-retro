from django.shortcuts import render, get_object_or_404
from .models import Informations

def info(request):
    message = get_object_or_404(Informations, pk=1)
    return render(request, 'maintenance/index.html', {'message': message})