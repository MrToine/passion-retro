from django.db import models
from users.models import User

class LittleBacGames(models.Model):
    id = models.AutoField(primary_key=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='games')
    name = models.CharField(max_length=155)
    status = models.CharField(max_length=20 ,choices=[
        ('waiting', 'En attente'),
        ('in_progress', 'En cours'),
        ('finished', 'Terminée')
    ], default='waiting')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    countdown_started = models.BooleanField(default=False)
    countdown_time = models.IntegerField(default=0)
    countdown_start_time = models.DateTimeField(default=None, null=True, blank=True)
    current_phase = models.CharField(max_length=60, default="ready_game", null=True, blank=True)

class LittleBacPlayers(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='players')
    game = models.ForeignKey(LittleBacGames, on_delete=models.CASCADE, related_name='players')
    score = models.IntegerField()
    is_ready = models.BooleanField(default=False)
    status = models.CharField(max_length=20, choices=[
        ('playing', 'Joue'),
        ('overed', 'A fini')
    ], default="playing")

class LittleBacCategories(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    description = models.TextField(default="")

class LittleBacRounds(models.Model):
    id = models.AutoField(primary_key=True)
    game = models.ForeignKey(LittleBacGames, on_delete=models.CASCADE, related_name='rounds')
    letter = models.CharField(max_length=1)
    round_counter = models.IntegerField(default=1)

class LittleBacAnswers(models.Model):
    id = models.AutoField(primary_key=True)
    round = models.ForeignKey(LittleBacRounds, on_delete=models.CASCADE, related_name='answers')
    player = models.ForeignKey(LittleBacPlayers, on_delete=models.CASCADE, related_name='answers')
    category = models.ForeignKey(LittleBacCategories, on_delete=models.CASCADE, related_name='answers')
    answer = models.CharField(max_length=100)
    is_valid = models.BooleanField(default=False)
    point = models.IntegerField(default=0)