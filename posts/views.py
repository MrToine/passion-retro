from django.shortcuts import render, get_object_or_404, redirect
from posts.models import Post
from forum.models import Topic, Forum, Post as ForumPost
from users.models import UserLevel
from django.contrib import messages
from users.decorators import groups_required
from posts.forms import CreatePost, EditPost
from django.utils.text import slugify
from django.contrib.auth.decorators import login_required
from django.db.models import F

def view_post(request, slug):
    post = Post.objects.filter(slug=slug, active=True).first()
    subposts = None

    if post.parent:
        subposts = Post.objects.filter(post_parent=post.id)

    context = {
        'post': post,
        'subposts': subposts
    }

    return render(request, "posts/post.html", context)

@groups_required('Rédacteur', 'Admininistrateur', 'Super Admin')
def create_post(request, type):
    # Create a new post
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        active = request.POST.get('active') == 'on'
        image=request.FILES.get('image') if type == 'news' else None

        # Si c'est une news, on créer aussi un topic sur le forum news
        if type == 'news':
            topic = Topic.objects.create(
                title=title,
                forum=Forum.objects.get(name='Actus du site'),
                author=request.user
            )

            content_forum = f'<p><img src="/media/images/{image}"></p><p>{content}</p>'

            forum_post = ForumPost.objects.create(
                topic=topic,
                content=content_forum,
                author=request.user
            )

            UserLevel.objects.update(user=request.user, experience=F('experience') + 20)

            topic.save()
            forum_post.save()

        forum_link = f'forum/{topic.forum.id}/{topic.id}/'
        
        post = Post.objects.create(
            slug=slugify(title),
            title=title,
            content=content,
            type=type,
            image=image,
            author=request.user,
            active=active,
            forum_link=forum_link
        )

        post.save()



        messages.success(request, 'Post créer avec succès !')

        return redirect('home')

    context = {
        'type': type,
        'post_form': CreatePost(),
    }

    return render(request, "posts/create_post.html", context)

@login_required()
def edit_post(request, post_id):
    post = get_object_or_404(Post, id=post_id, author=request.user)
    
    if request.method == 'POST':
        form = EditPost(request.POST, instance=post)
        if form.is_valid():
            post.title = form.cleaned_data['title']
            post.content = form.cleaned_data['content']
            post.active = False
            post.save()
            return redirect('contributions') 
    else:
        form = CreatePost(initial={
            'title': post.title,
            'content': post.content,
        })

    return render(request, 'posts/edit_post.html', {'form': form, 'post': post})

@groups_required('Administrateur', 'Super Admin')
def prending_posts(request):
    posts = Post.objects.filter(active=False)

    return render(request, 'posts/pending_posts.html')