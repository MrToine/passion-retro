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
from .models import User

def register(request):
    # Si l'utilisateur est deja connecté, on le redirige vers la page de profil
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
            activation_link = request.build_absolute_uri(f"/activate/{user.uid}/{token}")
            
            email_subject = 'Activation de votre compte'
            email_body = render_to_string('emails/activation_account.html', {
                'user': user,
                'activation_link': activation_link,
            })
            
            send_mail(
                email_subject,
                email_body,
                settings.EMAIL_HOST_USER,
                [user.email],
                fail_silently=False,
            )
            
            messages.success(request, f"Ton compte a été créé avec succès, {user.username}! Un email d'activation t'a été envoyé pour valider ton inscription.")

            return redirect('login')
    else:
        form = UserRegistrationForm()
    return render(request, 'users/register.html', {'form': form})

def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    token_generator = PasswordResetTokenGenerator()
    if user is not None and token_generator.check_token(user, token):
        user.is_active = True
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
            print(user)
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
    return render(request, 'users/profile.html')

def another_profile(request, user_id):
    user = User.objects.get(id=user_id)
    return render(request, 'users/profile.html', {'user': user})

@login_required(login_url='login')
def profile_update(request):
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
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
        form = PostForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data.get('title')
            content = form.cleaned_data.get('content')
            type = type
            author = request.user
            active = False
            if type == 'news':
                image = form.cleaned_data.get('image')
            else:
                image = None

            post = Post.objects.create(
                title=title,
                slug = slugify(title),
                content=content,
                type=type,
                author=author,
                active=active,
                image=image,
                contribution=True
            )

            post.save()

            # On envoi un email à l'admin
            send_mail(
                'Nouvelle contribution',
                f'Une nouvelle contribution a été proposée par {request.user}! Connectez-vous pour la valider.',
                settings.EMAIL_HOST_USER,
                [settings.EMAIL_HOST_USER],
                fail_silently=False,
            )

            messages.success(request, f"Merci pour votre contribution, {request.user}! Nous allons examiner votre proposition.")
            return redirect('contribute')
        else:
            messages.error(request, "Une erreur s'est produite.")

    context = {
        'type': type,
        'form': PostForm()
    }

    return render(request, "users/form_contribute.html", context)