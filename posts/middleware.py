from django.utils.deprecation import MiddlewareMixin
from .models import Post

class PostsMiddleware(MiddlewareMixin):
    def process_request(self, request):

        # On récupère tous les posts de type 'games'
        posts_games = Post.objects.filter(type='games', active=True, parent=True)

        # On récupère tous les posts de type 'movies'
        posts_movies = Post.objects.filter(type='movies', active=True, parent=True)

        # On récupère tous les posts de type 'music'
        posts_music = Post.objects.filter(type='music', active=True, parent=True)

        # On récupère tous les posts de type 'tech'
        posts_tech = Post.objects.filter(type='tech', active=True, parent=True)

        # on met tout ça dans l'objet request
        request.posts_games = posts_games
        request.posts_movies = posts_movies
        request.posts_music = posts_music
        request.posts_tech = posts_tech