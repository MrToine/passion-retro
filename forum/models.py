from django.db import models
from users.models import User

class Category(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Catégorie'
        verbose_name_plural = 'Catégories'

    def __str__(self):
        return f'ForumCategory({self.id}, {self.name}, {self.description})'

class Forum(models.Model):
    id = models.AutoField(primary_key=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Forum({self.id}, {self.category}, {self.name}, {self.description})'

class Topic(models.Model):
    id = models.AutoField(primary_key=True)
    forum = models.ForeignKey(Forum, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    state = models.CharField(max_length=10, default='open')

    def save(self, *args, **kwargs):
        if not self.id:
            self.state = 'open'
        super(Topic, self).save(*args, **kwargs)

    def __str__(self):
        return f'Topic({self.id}, {self.forum}, {self.title})'

    def is_unread(self, user):
        if not user.is_authenticated:
            return False
            
        last_read = TopicRead.objects.filter(
            user=user,
            topic=self
        ).first()

        if not last_read:
            return True

        last_post = Post.objects.filter(topic=self).order_by('-created').first()
        if not last_post:
            return False

        return last_post.created > last_read.last_read

class Post(models.Model):
    id = models.AutoField(primary_key=True)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name='posts')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='forum_author')
    content = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    type = models.CharField(max_length=10, default='post')
    active = models.BooleanField(default=True)

    def __str__(self):
        return f'Post({self.id}, {self.topic}, {self.author}, {self.content})'

class TopicRead(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    last_read = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['user', 'topic']

    def __str__(self):
        return f'TopicRead({self.id}, {self.topic}, {self.user})'