from django.db import models
from users.models import User

# Création d'une messagerie privée pour les membres
class PrivateMessageSubject(models.Model):
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    subject = models.CharField(max_length=100)
    is_read = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f'Sujet: {self.subject} (De: {self.sender.username} À: {self.receiver.username})'

class PrivateMessage(models.Model):
    id = models.AutoField(primary_key=True)
    subject = models.ForeignKey(PrivateMessageSubject, on_delete=models.CASCADE, related_name='messages')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author_messages', default=1)
    message = models.TextField()
    date_sent = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'{self.author.username} ({self.date_sent})'
    
    class Meta:
        verbose_name = 'Message privé'
        verbose_name_plural = 'Messages privés'
        ordering = ['-date_sent']