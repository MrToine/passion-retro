from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models

def user_avatar_path(instance, filename):
    return f'media/avatars/{instance.user.id}/{filename}'

class User(AbstractUser):
    avatar = models.ImageField(upload_to=user_avatar_path, default='media/avatars/default.gif')
    biography = models.TextField(default='Pas de bio')
    birth_date = models.DateField(null=True, blank=True)
    active = models.BooleanField(default=False)
    theme = models.CharField(max_length=50, default='default')

    groups = models.ManyToManyField(
        Group,
        related_name='customuser_set',  # Ajoutez un related_name unique
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups',
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='customuser_permissions_set',  # Ajoutez un related_name unique
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )

    def __str__(self):
        return self.username
    
    class Meta:
        verbose_name = 'Utilisateur'
        verbose_name_plural = 'Utilisateurs'
        ordering = ['username']
    
    