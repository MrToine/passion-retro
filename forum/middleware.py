from django.utils.deprecation import MiddlewareMixin
from .models import Forum, Topic, Post
from users.models import User
from django.db.models import Count

class ForumStatsMiddleware(MiddlewareMixin):
    # On récupère les statistiques du forum pour les affiché dans le menu
    def process_request(self, request):
        # Nombre total de forums
        total_forums = Forum.objects.count()

        # Nombre total de topics
        total_topics = Topic.objects.count()

        # Nombre total de posts
        total_posts = Post.objects.count()

        # Utilisateur ayant posté le plus de messages
        user_with_most_posts = User.objects.annotate(num_posts=Count('post')).order_by('-num_posts').first()

        # Nombre de messages de l'utilisateur ayant posté le plus de messages
        most_posts = user_with_most_posts.num_posts if user_with_most_posts else 0
        
        # Utilisateur ayant créé le plus de topics
        user_with_most_topics = None
        most_topics = 0
        for user in User.objects.all():
            if user.topic_set.count() > most_topics:
                user_with_most_topics = user
                most_topics = user.topic_set.count()
        
        # Dernier message posté
        last_post = Post.objects.latest('created') if total_posts > 0 else None

        # Derneir topic créé
        last_topic = Topic.objects.latest('created') if total_topics > 0 else None

        # Ajouter les variables à l'objet request
        request.total_forums = total_forums
        request.total_topics = total_topics
        request.total_posts = total_posts
        request.user_with_most_posts = user_with_most_posts
        request.most_posts = most_posts
        request.user_with_most_topics = user_with_most_topics
        request.most_topics = most_topics
        request.last_post = last_post
        request.last_topic = last_topic