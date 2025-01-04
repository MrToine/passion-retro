from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.utils import timezone
from .models import Category, Forum, Topic, Post, TopicRead
from .forms import CreateTopic, CreatePost, EditPost
from django.db.models import Max
from users.decorators import groups_required

def forum_home(request):
    categories = Category.objects.all()
    forums = Forum.objects.all()

    last_posts = {}
    count_topics = {}
    unread_topics = {}

    for forum in forums:
        # Dernier post du forum avec une seule requête
        last_post = Post.objects.select_related(
            'topic', 
            'author',
            'topic__forum'
        ).filter(
            topic__forum=forum
        ).order_by('-created').first()
        
        last_posts[forum.id] = last_post
        
        # Nombre de topics (pas de changement)
        count_topic = Topic.objects.filter(forum=forum).count()
        count_topics[forum.id] = count_topic

        # Optimisation de la vérification des topics non lus
        if request.user.is_authenticated:
            # Récupérer le dernier post de chaque topic du forum en une seule requête
            latest_posts_per_topic = Post.objects.filter(
                topic__forum=forum
            ).values('topic_id').annotate(
                last_post_date=Max('created')
            )
            
            # Récupérer les dernières lectures de l'utilisateur pour tous les topics du forum
            topic_reads = TopicRead.objects.filter(
                user=request.user,
                topic__forum=forum
            ).values_list('topic_id', 'last_read')
            
            # Convertir en dictionnaire pour un accès plus rapide
            read_dates = dict(topic_reads)
            
            # Un forum est non lu si au moins un topic a un post plus récent que la dernière lecture
            is_unread = False
            for post_info in latest_posts_per_topic:
                topic_id = post_info['topic_id']
                last_post_date = post_info['last_post_date']
                
                # Si le topic n'a jamais été lu
                if topic_id not in read_dates:
                    is_unread = True
                    break
                
                # Si le dernier post est plus récent que la dernière lecture
                if last_post_date > read_dates[topic_id]:
                    is_unread = True
                    break
            
            unread_topics[forum.id] = is_unread
        else:
            unread_topics[forum.id] = False

        print(unread_topics)
    
    context = {
        'categories': categories,
        'forums': forums,
        'last_posts': last_posts,
        'count_topics': count_topics,
        'unread_topics': unread_topics,
    }

    return render(request, "components/forum_home.html", context)

def topic_list(request, forum_id):
    forum = Forum.objects.get(id=forum_id)
    topics = Topic.objects.filter(forum=forum)
    paginator = Paginator(topics, 20)

    page_number = request.GET.get('page')
    topics = paginator.get_page(page_number)

    count_posts = {}
    last_posts = {}
    page_numbers = {}
    unread_topics = {}

    for topic in topics:
        count_post = Post.objects.filter(topic=topic).count()
        count_posts[topic.id] = count_post

        last_post = Post.objects.filter(topic=topic).order_by('-created').first()
        last_posts[topic.id] = last_post

        if request.user.is_authenticated:
            # Récupérer le dernier post du topic
            latest_post = Post.objects.filter(topic=topic).aggregate(last_post_date=Max('created'))['last_post_date']
            
            # Récupérer la dernière lecture de l'utilisateur pour ce topic
            topic_read = TopicRead.objects.filter(user=request.user, topic=topic).first()
            
            # Un topic est non lu si le dernier post est plus récent que la dernière lecture
            if topic_read:
                unread_topics[topic.id] = latest_post > topic_read.last_read
            else:
                unread_topics[topic.id] = True
        else:
            unread_topics[topic.id] = False

        if last_post:
            # Position du dernier message (nombre de messages jusqu'à ce message)
            post_position = Post.objects.filter(
                topic=topic,
                created__lte=last_post.created
            ).count()
            
            # Calcul du numéro de page (20 messages par page comme dans topic_detail)
            page_number = (post_position + 19) // 20  # équivalent à ceil(post_position/20)
            page_numbers[topic.id] = page_number

    context = {
        'forum': forum,
        'topics': topics,
        'count_posts': count_posts,
        'last_posts': last_posts,
        'page_numbers': page_numbers,
        'unread_topics': unread_topics,
        'is_paginated': topics.has_other_pages(),
        'page_obj': topics,
        'paginator': paginator,
    }

    return render(request, "forum/topic_list.html", context)

@login_required
def create_topic(request, forum_id):
    if not request.user.is_active:
        return HttpResponseForbidden("Vous n'êtes pas autorisé à créer un sujet.")
    
    if request.method == 'POST':
        topic_form = request.POST
        # On créer le topic via le model Topic
        topic = Topic(
            forum=Forum.objects.get(id=forum_id),
            author=request.user,
            title=topic_form['title'],
        )

        # Puis le premier post du topic
        post = Post(
            topic=topic,
            author=request.user,
            content=topic_form['content'],
        )

        topic.save()
        post.save()
        messages.success(request, 'Topic créer avec succès.')
        # on renvoie l'utilisateur sur la page du topic contenu l'id du forum et du topic créer
        return redirect('post_list', forum_id=forum_id, topic_id=topic.id)
    
    forum = Forum.objects.get(id=forum_id)
    topic_form = CreateTopic()
    context = {
        'forum': forum,
        'topic_form': topic_form,
    }
    return render(request, "forum/create_topic.html", context)

def topic_detail(request, topic_id, forum_id):
    if request.method == 'POST':
        if not request.user.is_active or not request.user.is_authenticated:
            return HttpResponseForbidden("Vous n'êtes pas autorisé à poster un message.")

        post_form = CreatePost(request.POST)
        if post_form.is_valid():
            post = Post(
                topic=Topic.objects.get(id=topic_id),
                author=request.user,
                content=post_form.cleaned_data['content'],
            )
            post.save()
            messages.success(request, 'Message posté avec succès.')
    
    topic = Topic.objects.get(id=topic_id)
    posts = Post.objects.filter(topic=topic, active=True)
    paginator = Paginator(posts, 20)

    page_number = request.GET.get('page')
    posts = paginator.get_page(page_number)

    # Marquer comme lu si l'utilisateur est connecté
    if request.user.is_authenticated:
        TopicRead.objects.update_or_create(
            user=request.user,
            topic=topic,
            defaults={'last_read': timezone.now()}
        )

    # On compte le nombre de posts de l'auteur
    count_posts = {}
    for post in posts:
        count_post = Post.objects.filter(author=post.author).count()
        count_posts[post.author.id] = count_post

    context = {
        'topic': topic,
        'posts': posts,
        'count_posts': count_posts,
        'post_form': CreatePost(),
        'is_paginated': posts.has_other_pages(),
        'page_obj': posts,
        'paginator': paginator,
    }

    return render(request, "forum/topic_detail.html", context)

@groups_required('Modérateur', 'Admininistrateur', 'Super Admin')
def lock_topic(request, topic_id):
    topic = Topic.objects.get(id=topic_id)
    topic.state = 'closed'
    topic.save()
    messages.success(request, 'Sujet verrouillé avec succès.')
    return redirect('post_list', forum_id=topic.forum.id, topic_id=topic_id)

@groups_required('Modérateur', 'Admininistrateur', 'Super Admin')
def unlock_topic(request, topic_id):
    topic = Topic.objects.get(id=topic_id)
    topic.state = 'open'
    topic.save()
    messages.success(request, 'Sujet déverrouillé avec succès.')
    return redirect('post_list', forum_id=topic.forum.id, topic_id=topic_id)

@groups_required('Modérateur', 'Admininistrateur', 'Super Admin')
def deactivate_post(request, post_id):
    post = Post.objects.get(id=post_id)
    post.active = False
    post.save()
    messages.success(request, 'Message désactivé avec succès.')
    return redirect('post_list', forum_id=post.topic.forum.id, topic_id=post.topic.id)

@groups_required('Modérateur', 'Admininistrateur', 'Super Admin')
def activate_post(request, post_id):
    post = Post.objects.get(id=post_id)
    post.active = True
    post.save()
    messages.success(request, 'Message activé avec succès.')
    return redirect('post_list', forum_id=post.topic.forum.id, topic_id=post.topic.id)

@groups_required('Modérateur', 'Admininistrateur', 'Super Admin')
def deactivate_topic(request, topic_id):
    topic = Topic.objects.get(id=topic_id)
    topic.active = False
    topic.save()
    messages.success(request, 'Sujet désactivé avec succès.')
    return redirect('topic_list', forum_id=topic.forum.id)

@groups_required('Modérateur', 'Admininistrateur', 'Super Admin')
def activate_topic(request, topic_id):
    topic = Topic.objects.get(id=topic_id)
    topic.active = True
    topic.save()
    messages.success(request, 'Sujet activé avec succès.')
    return redirect('topic_list', forum_id=topic.forum.id)

@login_required
def edit_post(request, post_id):
    post = Post.objects.get(id=post_id)
    
    # Vérifier si l'utilisateur a le droit d'éditer
    if not (request.user == post.author or request.user.groups.filter(name__in=['Administrateur', 'Super Admin']).exists()):
        return HttpResponseForbidden("Vous n'êtes pas autorisé à éditer ce message.")
    
    if request.method == 'POST':
        form = EditPost(request.POST)
        if form.is_valid():
            post.content = form.cleaned_data['content']
            post.updated = timezone.now()
            post.save()
            messages.success(request, 'Message modifié avec succès.')
            return redirect('post_list', forum_id=post.topic.forum.id, topic_id=post.topic.id)
    else:
        form = EditPost(initial={'content': post.content})
    
    context = {
        'form': form,
        'post': post
    }
    return render(request, "forum/edit_post.html", context)