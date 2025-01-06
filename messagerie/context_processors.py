from .models import PrivateMessageSubject, PrivateMessage
from django.db.models import Q

def pending_pm_count(request):
    if request.user.is_authenticated:
        # Filtrer les sujets de messages où l'utilisateur est soit le receiver soit le sender
        pm_subjects = PrivateMessageSubject.objects.filter(
            Q(receiver=request.user) | Q(sender=request.user)
        )
        
        # Initialiser le compteur de messages non lus
        count = 0
        
        # Parcourir chaque sujet de message
        for subject in pm_subjects:
            # Récupérer le dernier message du sujet
            last_message = subject.messages.order_by('-date_sent').first()
            
            # Vérifier si le dernier message n'est pas de l'utilisateur actuel et si le sujet n'est pas lu
            if last_message and last_message.author != request.user and not subject.is_read:
                count += 1
        
        return {'pending_pm_count': count}
    return {'pending_pm_count': 0}