from django.db import models
from users.models import User

class Chat(models.Model):
    id = models.AutoField(primary_key=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return f'Chat({self.id}, {self.author}, {self.content}, {self.created})'