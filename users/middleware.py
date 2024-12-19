# yourapp/middleware.py

from .models import User
from django.utils.deprecation import MiddlewareMixin
from django.utils import timezone

class UserStatsMiddleware(MiddlewareMixin):
    def process_request(self, request):
        # Nombre total d'utilisateurs
        total_users = User.objects.count()
        
        # Dernier utilisateur inscrit
        last_user = User.objects.latest('date_joined') if total_users > 0 else None
        
        # Nombre de visiteurs uniques actuels
        visitor_count = 0

        # Nombre de visiteurs uniques depuis la création du site
        total_visitor_count = 0

        # Si l'utilisateur est authentifié
        if request.user.is_authenticated:
            theme_active = request.user.theme
        else:
            theme_active = 'default'
        
        # Ajouter les variables à l'objet request
        request.total_users = total_users
        request.last_user = last_user
        print(f"dernier user : {request.last_user}")
        request.visitor_count = visitor_count
        request.total_visitor_count = total_visitor_count
        request.theme_active = theme_active