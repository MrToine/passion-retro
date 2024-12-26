from django.shortcuts import redirect
from django.urls import reverse
from django.contrib.auth import get_user

from .models import Informations

class MaintenanceMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not request.user.is_superuser and not request.path.startswith('/admin'):
            try:
                maintenance_info = Informations.objects.get(pk=1)
            except Informations.DoesNotExist:
                maintenance_info = None

            if maintenance_info and maintenance_info.is_active == True and not request.path.startswith(reverse('maintenance:info')):
                return redirect(reverse('maintenance:info'))

        response = self.get_response(request)
        return response