from django.db import models
from users.models import User

class Quiz(models.Model):
    id = models.AutoField(primary_key=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='quizzes')
    name = models.CharField(max_length=155)
    description = models.TextField(default="")
    image = models.ImageField(upload_to='quiz_images/', default='', blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class Question(models.Model):
    id = models.AutoField(primary_key=True)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='questions')
    question = models.CharField(max_length=255)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.question

class Choice(models.Model):  # Renommé au singulier
    id = models.AutoField(primary_key=True)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='choices')
    choice = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.choice

class UserQuiz(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_quizzes')
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='user_quizzes')  # Ajouté
    score = models.IntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - {self.quiz.name}"

class UserAnswer(models.Model):
    id = models.AutoField(primary_key=True)
    user_quiz = models.ForeignKey(UserQuiz, on_delete=models.CASCADE, related_name='user_answers')
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='user_answers')
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE, related_name='user_answers')

    def __str__(self):
        return f"{self.user_quiz.user.username} - {self.question.question}"

    class Meta:
        unique_together = ('user_quiz', 'question')  # Empêche qu'un utilisateur réponde plusieurs fois à la même question.