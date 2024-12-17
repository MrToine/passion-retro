from django.utils.deprecation import MiddlewareMixin
from guestbook.models import Guestbook

class GuestbookMiddleware(MiddlewareMixin):
    def process_request(self, request):
        # On récupère les messages du livre d'or et les auteurs
        guestbook = Guestbook.objects.all().order_by('-created')[:5]

        # On compte le nombre de messages
        total_guestbook = Guestbook.objects.count()

        # On ajoute les variables à l'objet request
        request.guestbook = guestbook
        request.total_guestbook = total_guestbook