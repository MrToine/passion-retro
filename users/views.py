from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import PostForm, UserRegistrationForm, UserLoginForm, UserUpdateForm, ProfileUpdateForm
from posts.models import Post
from django.utils.text import slugify
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from .models import User, UserLevel
from django.db.models import F
import urllib.request
import json

def register(request):
    from messagerie.models import PrivateMessageSubject, PrivateMessage
    if request.user.is_authenticated:
        return redirect('profile')
    
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        recaptcha = request.POST.get('g-recaptcha-response')
        if form.is_valid():

            url = 'https://www.google.com/recaptcha/api/siteverify'
            values = {
                'secret': settings.GOOGLE_PRIVATE_KEY,
                'response': recaptcha
            }
            data = urllib.parse.urlencode(values).encode()
            req =  urllib.request.Request(url, data=data)
            response = urllib.request.urlopen(req)
            result = json.loads(response.read().decode())

            if result['success']:
                user = User.objects.create_user(
                    username=form.cleaned_data['username'],
                    email=form.cleaned_data['email'],
                    password=form.cleaned_data['password1'],
                    theme='00s',
                    active=True
                )

                messages.success(request, f"Bonjour et bienvenue {user.username} ! Ton compte à été créer avec succès. Tu peux désormais te connecter.")

                subject = PrivateMessageSubject.objects.create(
                    receiver=user,
                    sender=User.objects.get(username='RetroBot'),
                    subject="Bienvenue sur PassionRetro !"
                )

                PrivateMessage.objects.create(
                    subject=subject,
                    author=User.objects.get(username='RetroBot'),
                    message=f"""[b]Bienvenue sur Passion Retro ![/b]

Salut [b]{user.username}[/b] !,

Merci de nous avoir rejoints dans cette aventure dédiée aux passionnés de rétro ! Que tu sois fan de consoles vintage, collectionneur d'objets d'époque ou simple curieux, tu es ici chez toi. 

✨ [b]Découvre tout ce que Passion Retro a à offrir :[/b]  
Plonge dans nos articles pour en apprendre plus sur les trésors du passé, participe aux discussions sur le forum et teste tes connaissances avec nos jeux rétro. Chaque section est là pour te permettre de partager ta passion et d'en apprendre davantage.  

🚀 [b]Rejoins la communauté :[/b]  
Ton avis et tes contributions sont précieux ! N’hésite pas à lancer une discussion sur le forum, à réagir aux articles ou à défier les autres membres sur nos jeux. Plus nous sommes actifs, plus l’expérience sera enrichissante pour tous.  

Si tu as des questions ou des suggestions pour améliorer le site, contacte-nous. Nous sommes là pour t'accompagner !  

Encore une fois, bienvenue parmi nous et prépare-toi à replonger dans l’univers du rétro !  

À bientôt,  
[b]L'équipe Passion Retro[/b]""")

                return redirect('login')
            else:
                messages.error(request, f"On y est presque ! Vérifie bien le captcha pour finaliser ton inscription.")            

    form = UserRegistrationForm()
    return render(request, 'users/register.html', {'form': form, 'GOOGLE_PUBLIC_KEY': settings.GOOGLE_PUBLIC_KEY})

def register_with_token(request):
    # Si l'utilisateur est deja connecté, on le redirige vers la page de pr>
    if request.user.is_authenticated:
        return redirect('profile')
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password1']
            )
            genToken = PasswordResetTokenGenerator()
            token = genToken.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))

            activation_link = request.build_absolute_uri(f"/users/activate/{uid}/{token}")
           
            email_subject = 'Activation de votre compte'
            email_body = render_to_string('emails/activation_account.html', {
                'user': user,
                'activation_link': activation_link,
            })

            send_mail(
                email_subject,
                email_body,
                settings.DEFAULT_FROM_EMAIL,
                [user.email],
                fail_silently=False,
            )

            messages.success(request, f"Ton compte a été créé avec succès, {user.username}! Un email d'activation t'a été envoyé pour valider ton inscription.")

            return redirect('login')
    else:
        form = UserRegistrationForm()
    return render(request, 'users/register.html', {'form': form})

def activate(request, uidb64, token):
    uid = None  # Initialisation de la variable uid
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    token_generator = PasswordResetTokenGenerator()
    if user is not None and token_generator.check_token(user, token):
        user.active = True
        user.save()
        messages.success(request, "Votre compte a été activé avec succès.")
        return redirect('login')
    else:
        messages.error(request, "Le lien d'activation est invalide.")
        return redirect('register')

def login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is None:
                messages.error(request, "Nom d'utilisateur ou mot de passe incorrect.")
                return redirect('login')
            
            if user.active == False:
                messages.error(request, "Votre compte n'est pas activé. Veuillez vérifier votre boîte mail.")
                return redirect('login')
            
            auth_login(request, user)
            messages.success(request, f"Bienvenue, {username}!")
            return redirect('home')
        else:
            messages.error(request, "Nom d'utilisateur ou mot de passe incorrect.")
    else:
        form = UserLoginForm()
    
    return render(request, 'users/login.html', {'form': form})

def profile(request):
    from forum.models import Topic, Post
    from posts.models import Post
    user = User.objects.get(id=request.user.id)
    # On compte le nombre de topics du forum de l'utilisateur
    topics = Topic.objects.filter(author=user).count()
    forum_posts = Post.objects.filter(author=user).count()
    posts = Post.objects.filter(author=user).count()

    return render(request, 'users/profile.html', { 'user': user, 'topics': topics, 'forum_posts': forum_posts, 'posts': posts })

def another_profile(request, user_id):
    from forum.models import Topic, Post
    from posts.models import Post
    user = User.objects.get(id=user_id)
    # On compte le nombre de topics du forum de l'utilisateur
    topics = Topic.objects.filter(author=user).count()
    forum_posts = Post.objects.filter(author=user).count()
    posts = Post.objects.filter(author=user).count()

    return render(request, 'users/profile.html', {'user': user, 'topics': topics, 'forum_posts': forum_posts, 'posts': posts})

@login_required(login_url='login')
def profile_update(request):
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, request.FILES, instance=request.user)
        if user_form.is_valid():
            user_form.save()
            messages.success(request, 'Votre profil a été mis à jour avec succès !')
            return redirect('profile')
    else:
        user_form = UserUpdateForm(instance=request.user)
    return render(request, 'users/profile_update.html', {'user_form': user_form})

@login_required
def contribute(request):
    return render(request, "users/contribute.html")

@login_required(login_url='register')
def form_contribute(request, type):
    if request.method == 'POST':
        # Initialisation des articles
        form = PostForm(request.POST)
        posts = []

        # Traite l'article principal (parent)
        main_title = request.POST.get('title')  # Titre principal du formulaire Django
        main_content = request.POST.get('content')  # Contenu principal
        parent_post = None

        if main_title and main_content:
            # Crée le parent
            parent_post = Post.objects.create(
                title=main_title,
                slug=slugify(main_title),
                content=main_content,
                type=type,
                author=request.user,
                contribution=True,
                parent=True
            )
            posts.append(parent_post)
            UserLevel.objects.update(user=request.user, experience=F('experience') + 10)

        # Vérifie si des articles dynamiques existent (type_form = multiple)
        type_form = request.POST.get('type_form')

        if type_form == 'multiple':
            # Parcourt les champs dynamiques ajoutés en JS
            for key in request.POST:
                if key.startswith('title-post-'):
                    # Récupère le numéro de l'article
                    article_number = key.split('-')[-1]

                    # Récupère les données de l'article enfant
                    title = request.POST.get(f'title-post-{article_number}')
                    content = request.POST.get(f'content-post-{article_number}')

                    if title and content:
                        # Crée l'article enfant
                        child_post = Post.objects.create(
                            title=title,
                            slug=slugify(title),
                            content=content,
                            type=type,
                            author=request.user,
                            contribution=True,
                            parent=False,
                            post_parent=parent_post
                        )
                        posts.append(child_post)
                        UserLevel.objects.update(user=request.user, experience=F('experience') + 5)

        messages.success(request, "Vos articles ont été soumis avec succès !")

    context = {
        'type': type,
        'form': PostForm(),
    }
    return render(request, "users/form_contribute.html", context)

@login_required()
def contributions(request):
    posts = Post.objects.filter(author=request.user)

    return render(request, "users/contributions.html", {'posts':posts})

@login_required
def new_feature_user_level(request):
    # On créer une entree dans la table user_level pour l'utilisateur si il n'en a pas
    if not request.user.level:
        request.user.levels.create(level=1)
    return render(request, "features/new_feature_user_level.html")