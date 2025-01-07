from django.db import models

# Create your models here.
class Item(models.Model):
    category = models.ForeignKey('Category', on_delete=models.CASCADE, related_name='items')
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=5, decimal_places=2)
    image = models.ImageField(upload_to='shop/items/')
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='items_categories/')
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name