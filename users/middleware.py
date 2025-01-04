# yourapp/middleware.py

from django.core.cache import cache
from django.utils import timezone
from .models import User, VisitorStats
from django.utils.deprecation import MiddlewareMixin

class UserStatsMiddleware(MiddlewareMixin):
    def process_request(self, request):
        # Nombre total d'utilisateurs
        total_users = User.objects.count()
        
        # Dernier utilisateur inscrit
        last_user = User.objects.latest('date_joined') if total_users > 0 else None
        
        # Gestion des visiteurs actuels
        current_time = timezone.now()
        visitor_key = request.session.session_key or request.META.get('REMOTE_ADDR')
        
        # Mise à jour du cache des visiteurs actuels
        active_visitors = cache.get('active_visitors', set())
        active_visitors.add(visitor_key)
        cache.set('active_visitors', active_visitors, 300)  # expire après 5 minutes
        visitor_count = len(active_visitors)

        # Gestion du total des visiteurs
        stats, created = VisitorStats.objects.get_or_create(pk=1)
        if 'first_visit' not in request.session:
            request.session['first_visit'] = True
            stats.total_visitors += 1
            stats.save()
        total_visitor_count = stats.total_visitors

        # Si l'utilisateur est authentifié
        if request.user.is_authenticated:
            theme_active = request.user.theme
        else:
            theme_active = 'default'
        
        # Ajouter les variables à l'objet request
        request.total_users = total_users
        request.last_user = last_user
        request.visitor_count = visitor_count
        request.total_visitor_count = total_visitor_count
        request.theme_active = theme_active