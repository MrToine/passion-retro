# yourapp/middleware.py
from django.shortcuts import redirect
from django.core.cache import cache
from django.utils import timezone
from .models import User, VisitorStats
from messagerie.models import PrivateMessage, PrivateMessageSubject
from django.utils.deprecation import MiddlewareMixin
from django.contrib import messages

# On vérifie que l'user existe dans la table  user_level. Si pas, on le redirige vers la page tuto de la nouvelle feature
class UserLevelMiddleware(MiddlewareMixin):
    # On vérifie que l'on est pas sur la page de tuto de la nouvelle feature
    def process_request(self, request):
        if request.user.is_authenticated:
            if request.path != '/users/new/feature':
                if not request.user.levels.exists():
                    return redirect('new_feature_user')
            
            if request.path != '/users/new/feature':
                if not request.user.inventory.exists():
                    return redirect('new_feature_user')

class UserLevelUpMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if request.user.is_authenticated:
            if request.user.levels.exists():
                # On augmente le niveau de l'utilisateur si son expérience est suffisante. level 2: 100xp, pour les levels suivants: (level * 10) + (level + 20)
                if request.user.is_authenticated:
                    user = request.user
                    user_level = user.level  # Accède à l'objet UserLevel associé à l'utilisateur
                    
                    # Calcul de l'XP requise pour le prochain niveau
                    def xp_required(level):
                        return int(33.33 * (level ** 2) - 16.66 * level)

                    if user_level.experience >= xp_required(user_level.level):
                        user_level.level += 1
                        user_level.save()
                        messages.success(request, f"Bravo ! Vous avez atteint le niveau {user_level.level} !")
                        
                        subject = PrivateMessageSubject.objects.create(
                            receiver=user,
                            sender=User.objects.get(username='RetroBot'),
                            subject=f"Bravo { request.user } ! Tu as atteint un nouveau niveau !"
                        )

                        PrivateMessage.objects.create(
                            subject=subject,
                            author=User.objects.get(username='RetroBot'),
                            message=f"""[b]🎉 Félicitations {request.user}! 🎉[/b]

                                Tu viens de passer au [b]Niveau Supérieur[/b] ! Tu es maintenant [b]Niveau { user_level.level }[/b] !

                                💰 En récompense, tu gagnes [b]20 Or[/b] ! 💰

                                [i]Continue tes efforts, aventurier, et vise toujours plus haut ![/i]

                                [b]RetroBot IV, de Retronia[/b]"""
                        )
                    
                        if request.user.inventory.exists():
                            inventory_item = request.user.inventory.get(item__name='Or')
                            inventory_item.quantity += 20
                            inventory_item.save()
                        

                    # On affiche l'experience restante pour le prochain niveau
                    if user_level:
                        request.user.experience_left = xp_required(user_level.level) - user_level.experience

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
            theme_active = '00s'
        
        # Ajouter les variables à l'objet request
        request.total_users = total_users
        request.last_user = last_user
        request.visitor_count = visitor_count
        request.total_visitor_count = total_visitor_count
        request.theme_active = theme_active