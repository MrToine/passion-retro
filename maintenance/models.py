from django.db import models

class Informations(models.Model):
    name = models.CharField("Titre de la maintenance", max_length=255, default="Maintenance en cours")
    content = models.TextField(default="Votre site rétro favoris fait un chek-up ;)")
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return "Contenu de la maintenance"
    