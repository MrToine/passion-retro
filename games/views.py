from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import *
from django.utils.timezone import now
from django.contrib import messages
from django.db.models import Count
from django.db.models.functions import Lower

def portal(request):
    games = LittleBacGames.objects.filter(author=request.user, status='waiting')
    last_party = LittleBacGames.objects.filter().last()
    nb_parties = LittleBacGames.objects.filter(status="finished").count()
    return render(request, 'games/portal.html', {'games': games, 'last_party': last_party, 'nb_parties': nb_parties})

def little_bac_home(request):
    return render(request, 'games/littlebac/home.html')

@login_required()
def little_bac_start(request):
    import random
    import string
    
    game = LittleBacGames.objects.create(name=f"Partie de {request.user.username}", author=request.user)
    LittleBacPlayers.objects.create(
        user=request.user,
        game=game,
        score=0
    )

    
    # Liste des lettres de l'alphabet
    alphabet = string.ascii_uppercase  # 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

    # Sélection aléatoire
    random_letter = random.choice(alphabet)

    LittleBacRounds.objects.create(
        game=game,
        letter=random_letter,
        round_counter=1
    )

    return redirect('bac_party_games', party_id=game.id)

@login_required()
def little_bac_party(request, party_id):
    game = LittleBacGames.objects.get(id=party_id)
    players = LittleBacPlayers.objects.filter(game=game)
    
    if players.filter(user=request.user).exists():
        return render(request, 'games/littlebac/game.html', {'game': game, 'players': players})
    else:
        return redirect('bac_games')

@login_required()
def little_bac_party_join(request, party_id):
    game = LittleBacGames.objects.get(id=party_id)
    players = LittleBacPlayers.objects.filter(game=game)
    
    if players.filter(user=request.user).exists():
        return redirect('bac_games')

    LittleBacPlayers.objects.create(
        user=request.user,
        game=game,
        score=0
    )

    return redirect('bac_party_games', party_id=game.id)    

@login_required()
def little_bac_party_play(request, party_id):
    game = LittleBacGames.objects.get(id=party_id)
    players = LittleBacPlayers.objects.filter(game=game)
    
    if not players.filter(user=request.user).exists():
        return redirect('bac_games')

    # Vérifie si la partie est en attente et met à jour le statut
    if game.status == 'waiting':
        game.status = 'in_progress'
        game.save()

    round = LittleBacRounds.objects.filter(game=game).first()  # Utilisation de .first() pour éviter IndexError
    categories = LittleBacCategories.objects.all()

    if request.method == "POST":
        print("POST")
        # On vérifie que les réponses commencent par la lettre du round
        round_letter = round.letter.upper()
        all_valid = True
        for category in categories:
            answer = request.POST.get(f"col-{category.id}", "").strip()
            if answer and answer[0].upper() != round_letter:
                all_valid = False
                break
        
        if all_valid:
            player = LittleBacPlayers.objects.get(game=game, user_id=request.user.id)
            player.status = "overed"
            player.save()

            # Récupérer les réponses soumises par le joueur
            answers = {
                f"col-{category.id}": request.POST.get(f"col-{category.id}")
                for category in categories
            }

            responses = []
            # Enregistre chaque réponse en base de données
            for category in categories:
                answer = answers.get(f"col-{category.id}", "").strip()  # Récupère la réponse ou une chaîne vide
                if answer:  # Vérifie si une réponse est fournie
                    response = LittleBacAnswers.objects.create(
                        round=round,
                        player=players.get(user=request.user),
                        category=category,
                        answer=answer,
                        is_valid=False
                    )
                    responses.append(response)

            return render(request, 'games/littlebac/finish.html', {'responses': responses, 'round': round, 'categories': categories})
        else:
            messages.error(request, "Les réponses doivent commencer par la lettre du tour.")
            return render(request, 'games/littlebac/play.html', {
                'game': game,
                'round': round,
                'categories': categories,
                'countdown_remaining': countdown_remaining,
        })

    # Passe les informations du décompte au template
    countdown_remaining = max(
        0, game.countdown_time - int((now() - game.countdown_start_time).total_seconds())
    ) if game.countdown_started else None

    return render(request, 'games/littlebac/play.html', {
        'game': game,
        'round': round,
        'categories': categories,
        'countdown_remaining': countdown_remaining
    })

login_required()
def game_little_bac_results(request, party_id):
    game = LittleBacGames.objects.get(id=party_id)
    players = LittleBacPlayers.objects.filter(game=game)
    rounds = LittleBacRounds.objects.filter(game=game)
    categories = LittleBacCategories.objects.all()
    answers = LittleBacAnswers.objects.filter(round__game=game)

    # On détermine qu'un mot est valide si il est unique pour une catégorie donnée
    for round in rounds:
        for category in categories:
            valid_answers = answers.filter(round=round, category=category).annotate(
                lower_answer=Lower('answer')
            ).values('lower_answer').annotate(
                count=Count('lower_answer')
            ).filter(count=1)
            for answer in valid_answers:
                answers.filter(round=round, category=category, answer__iexact=answer['lower_answer']).update(is_valid=True)

    # Calcule des points pour chaque joueur. Si il a donné une réponse valide, il gagne 5 points, si il a la même réponse qu'un autre joueur, il gagne 1 points
    for player in players:
        player.score = 0
        for round in rounds:
            player_answers = LittleBacAnswers.objects.filter(round=round, player=player)
            for answer in player_answers:
                if LittleBacAnswers.objects.filter(round=round, answer=answer.answer, is_valid=True):
                    player.score += 5
                else:
                    player.score += 1
        player.save()

    # Organiser les réponses par joueur et par catégorie
    organized_answers = {}
    for player in players:
        organized_answers[player.id] = {}
        for category in categories:
            answer = answers.filter(player=player, category=category).first()
            organized_answers[player.id][category.id] = answer.answer if answer else ""

    return render(request, 'games/littlebac/results.html', {
        'game': game,
        'players': players,
        'rounds': rounds,
        'categories': categories,
        'organized_answers': organized_answers
    })

# API REST DES JEUX
@login_required()
def game_players_little_bac(request, game_id):
    try:
        game = LittleBacGames.objects.get(id=game_id)
        players = LittleBacPlayers.objects.filter(game=game)
        players_list = [{"id": player.id, "username": player.user.username, "score": player.score} for player in players]
        return JsonResponse({"game_id": game_id, "players": players_list})
    except LittleBacGames.DoesNotExist:
        return JsonResponse({"error": "Game not found"}, status=404)

@login_required()
def toggle_ready_status_little_bac(request, game_id, player_id):
    try:
        game = LittleBacGames.objects.get(id=game_id)
        player = LittleBacPlayers.objects.get(game=game, user_id=player_id)

        player.is_ready = not player.is_ready
        player.save()

        # Vérifie si tous les joueurs de la partie sont prêts
        game = player.game
        print("Joueurs de la partie",game)
        all_ready = LittleBacPlayers.objects.filter(game=game, is_ready=True).count()
        print(all_ready)

        return JsonResponse({"is_ready": player.is_ready, "all_ready": all_ready})
    except LittleBacPlayers.DoesNotExist:
        return JsonResponse({"error": "Player not found"}, status=404)

def game_infos_little_bac(request, game_id):
    try:
        game = LittleBacGames.objects.get(id=game_id)

        return JsonResponse({
            "name": game.name, 
            "status": game.status,
            "created": game.created,
            "all_ready": game.players.filter(is_ready=True).count()
        })
    except LittleBacGames.DoesNotExist:
        return JsonResponse({"error": "Party not found"}, status=404)

@login_required()
def party_infos_little_bac(request, game_id):
    from django.utils.timezone import now

    try:
        game = LittleBacGames.objects.get(id=game_id)
        players = LittleBacPlayers.objects.filter(game=game)
        players_data = [
            {"id": player.id, "username": player.user.username, "status": player.status, "score": player.score}
            for player in players
        ]

        countdown_remaining = None
        if game.countdown_started and game.countdown_start_time:
            elapsed_time = (now() - game.countdown_start_time).total_seconds()
            countdown_remaining = max(0, game.countdown_time - int(elapsed_time))

        print(game.status)

        return JsonResponse({
            "game_status": game.status,
            "players": players_data,
            "countdown_time": countdown_remaining,
            "countdown_started": game.countdown_started,
            "current_phase": game.current_phase if hasattr(game, 'current_phase') else None
        })
    except LittleBacGames.DoesNotExist:
        return JsonResponse({"error": "Game not found"}, status=404)
    
@login_required()
def game_start_countdown(request, game_id):
    from django.utils.timezone import now

    # Récupère le type de décompte (ready_game ou finish_game)
    countdown_type = request.GET.get("type", "ready_game")
    print(f"Type de décompte reçu: {countdown_type}")  # Ajout de cette ligne pour vérifier le type de décompte

    if countdown_type not in ["ready_game", "finish_game"]:
        return JsonResponse({"success": False, "error": "Type de décompte invalide."}, status=400)

    try:
        game = LittleBacGames.objects.get(id=game_id)
        print(f"Statut du jeu: {game.status}")  # Ajout de cette ligne pour vérifier le statut du jeu

        # Vérification des conditions pour chaque décompte
        if countdown_type == "ready_game" and not game.countdown_started and game.status == "waiting":
            game.countdown_started = True
            game.countdown_start_time = now()
            game.countdown_time = 5
            game.save()

        elif countdown_type == "finish_game" and game.status == "in_progress":
            print("Finish game")
            # Vérifie si un décompte précédent n'est pas actif
            elapsed_time = (now() - game.countdown_start_time).total_seconds()
            if not game.countdown_started or elapsed_time >= game.countdown_time:
                print("Start countdown")
                game.countdown_started = True
                game.countdown_start_time = now()
                game.countdown_time = 60
                game.current_phase = "finish_game"
                game.save()
            else:
                return JsonResponse({"success": False, "error": "Décompte déjà en cours."}, status=400)

        else:
            return JsonResponse({"success": False, "error": "Condition de décompte non remplie."}, status=400)

        return JsonResponse({
            "success": True,
            "countdown_started": game.countdown_started,
            "countdown_time": game.countdown_time
        })
    except LittleBacGames.DoesNotExist:
        return JsonResponse({"success": False, "error": "Game not found"}, status=404)

def game_countdown_status(request, game_id):
    from django.utils.timezone import now

    game = LittleBacGames.objects.get(id=game_id)

    if game.countdown_started and game.countdown_start_time:
        # Temps écoulé en secondes
        elapsed_time = (now() - game.countdown_start_time).total_seconds()
        remaining_time = max(0, game.countdown_time - int(elapsed_time))
        print(f"Elapsed time: {elapsed_time}, Remaining time: {remaining_time}")  # Vérification
    else:
        print("Ouuups")
        remaining_time = game.countdown_time

    return JsonResponse({
        "countdown_started": game.countdown_started,
        "countdown_time": remaining_time
    })

@login_required()
def game_liitle_bac_end_game(request, game_id):
    from django.utils.timezone import now

    try:
        game = LittleBacGames.objects.get(id=game_id)

        # Mettre à jour l'état du jeu à "finished"
        game.status = 'finished'
        game.updated = now()
        game.save()

        # Optionnel : Mettez à jour tous les joueurs pour les marquer comme ayant terminé
        LittleBacPlayers.objects.filter(game=game).update(status='overed')

        return JsonResponse({"success": True, "message": "Game ended successfully."})
    except LittleBacGames.DoesNotExist:
        return JsonResponse({"error": "Game not found"}, status=404)