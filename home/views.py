from django.shortcuts import render
from posts.models import Post

def home(request):
    edito = Post.objects.filter(type='edito', active=True).first()
    news = Post.objects.filter(type='news', active=True).order_by('-created')[:6]

    context = {
        'edito': edito,
        'news': news,
    }

    return render(request, "home.html", context)