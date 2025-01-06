from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import PrivateMessage, PrivateMessageSubject
from django.db import models
from django.db.models import Max
from .forms import PrivateMessageForm, PrivateMessageSubjectForm
from django.contrib import messages

@login_required
def home(request):
    private_messages = PrivateMessageSubject.objects.filter(
        (models.Q(receiver=request.user) | models.Q(sender=request.user)) & models.Q(is_active=True)
    ).annotate(last_message_date=Max('messages__date_sent')).order_by('-last_message_date')

    return render(request, 'messagerie/home.html', {'private_messages': private_messages})

@login_required
def view_message(request, message_id):
    pm_message = PrivateMessageSubject.objects.get(pk=message_id)
    if (pm_message.receiver != request.user and pm_message.sender != request.user) or not pm_message.is_active:
        return redirect('pm_home')

    private_messages = PrivateMessage.objects.filter(subject=pm_message).order_by('date_sent')

    form = PrivateMessageForm(request.POST or None)

    if not pm_message.is_read and pm_message.messages.first().author != request.user:
        pm_message.is_read = True
        pm_message.save()
    
    if form.is_valid():
        message = form.save(commit=False)
        message.author = request.user
        message.subject = pm_message
        message.save()
        
        pm_message.is_read = False
        pm_message.save()

        form = PrivateMessageForm()

        return render(request, 'messagerie/view_message.html', {'pm_message': pm_message, 'private_messages': private_messages, 'form': form})

    return render(request, 'messagerie/view_message.html', {'pm_message': pm_message, 'private_messages': private_messages, 'form': form})

@login_required
def new_message(request):
    form_subject = PrivateMessageSubjectForm(request.POST or None)
    form_message = PrivateMessageForm(request.POST or None)

    if form_subject.is_valid() and form_message.is_valid():
        if form_subject.cleaned_data['receiver'] == request.user:
            messages.error(request, 'Vous ne pouvez pas vous envoyer un message à vous-même')
            return redirect('pm_home')
        subject = form_subject.save(commit=False)
        subject.sender = request.user
        subject.is_read = False
        subject.save()

        message = form_message.save(commit=False)
        message.author = request.user
        message.subject = subject
        message.save()

        return redirect('pm_view', message_id=message.id)

    return render(request, 'messagerie/new_message.html', {'form_subject': form_subject, 'form_message': form_message})

def delete_subject(request, message_id):
    pm_message = PrivateMessageSubject.objects.get(pk=message_id)
    if pm_message.receiver != request.user and pm_message.sender != request.user:
        return redirect('pm_home')
    
    pm_message.is_active = False
    pm_message.is_read = True
    pm_message.save()

    messages.success(request, 'Le sujet a bien été supprimé')

    return redirect('pm_home')

@login_required
def send_all_users(request):
    from users.models import User
    all_users = User.objects.all()
    sender = User.objects.get(username='RetroBot')
    for user in all_users:
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

        subject = PrivateMessageSubject.objects.create(receiver=user, sender=sender, subject='Bienvenue sur la messagerie privée')
        PrivateMessage.objects.create(
            subject=subject, 
            author=sender, 
            message=f"Cher [b]{user.username}[/b],\n\nBienvenue sur la messagerie privée de passion-retro. Tu peux désormais échanger des messages privés avec les autres membres du site.\n\nQuant a moi, je suis un nouvel utilisateur du site venu de la planète [b]Retronia[/b] ! J'ai été investis de la mission la plus importante de ma longue vie : [u]être le meilleur assistant de passion-retro[/u] ! J'espère sincèrement y parvenir !\n\nJe suis encore en orbite actuellement, mais guette les infos car je serait bientôt présent !\n\nCordialement,\n{sender.username}"
        )
    return redirect('pm_home')