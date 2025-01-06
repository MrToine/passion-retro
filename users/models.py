from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models

def user_avatar_path(instance, filename):
    return f'avatars/{instance.id}/{filename}'

class User(AbstractUser):
    avatar = models.ImageField(upload_to=user_avatar_path, default='avatars/default.gif')
    email = models.EmailField(unique=False)
    biography = models.TextField(default='Pas de bio')
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
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

    @property
    def level(self):
        return self.levels.first()
    
    @property
    def experience(self):
        return self.levels.get(user=self).experience
    
    @property
    def money(self):
        return self.levels.get(user=self).money

    def __str__(self):
        return self.username
    
    class Meta:
        verbose_name = 'Utilisateur'
        verbose_name_plural = 'Utilisateurs'
        ordering = ['username']

class VisitorStats(models.Model):
    total_visitors = models.PositiveIntegerField(default=0)
    last_reset = models.DateTimeField(auto_now=True)

class UserLevel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='levels')
    level = models.PositiveIntegerField(default=1)
    experience = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.level

    class Meta:
        verbose_name = 'Niveau utilisateur'
        verbose_name_plural = 'Niveaux utilisateurs'
        ordering = ['level']