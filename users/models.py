from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from shop.models import Item

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
    border_avatar = models.CharField(max_length=50, blank=True, null=True)
    username_decoration = models.CharField(max_length=50, blank=True, null=True)

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
    def inventory(self):
        return self.inventory.all()
    
    @property
    def money(self):
        return self.inventory.get(item__name='Or').quantity

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

class UserInventory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='inventory')
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return self.item.name

    class Meta:
        verbose_name = 'Inventaire utilisateur'
        verbose_name_plural = 'Inventaires utilisateurs'
        ordering = ['item']