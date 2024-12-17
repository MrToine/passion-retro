from django.db import models
from users.models import User

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

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'