from django.db import models
from users.models import User
from commons.bbcode_parser import BBCodeParser
from django.db.models.signals import pre_delete
from django.dispatch import receiver

class Category(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Categorie'
        verbose_name_plural = 'Categories'

class Post(models.Model):
    id = models.AutoField(primary_key=True)
    slug = models.SlugField(max_length=200, unique=True, default='default-slug')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=1)
    title = models.CharField(max_length=200)
    content = models.TextField()
    type = models.CharField(max_length=200, default='news')
    image = models.ImageField(upload_to='images/', null=True, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    active = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    contribution = models.BooleanField(default=False)
    forum_link = models.CharField(max_length=200, null=True, blank=True)
    post_parent = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='child_posts')
    parent = models.BooleanField(default=True)

    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        # Si le post a un parent, il ne doit pas être considéré comme parent
        if self.post_parent:
            self.parent = False
        else:
            self.parent = True
        super().save(*args, **kwargs)
    
    
    class Meta:
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'
    
@receiver(pre_delete, sender=Post)
def handle_parent_deletion(sender, instance, **kwargs):
    # Si le post supprimé a des enfants
    for child in instance.child_posts.all():
        # Rendre l'enfant un parent
        child.post_parent = None
        child.parent = True
        child.save()