from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import *
from django.utils.timezone import now
from django.contrib import messages
from django.db.models import Count, Sum
from django.db.models.functions import Lower

def portal(request):
    last_party = LittleBacGames.objects.filter().last()
    nb_parties = LittleBacGames.objects.filter(status="finished").count()
    
    if not request.user.is_authenticated:
        return render(request, 'games/portal.html', {'last_party': last_party, 'nb_parties': nb_parties})
    games = LittleBacGames.objects.filter(author=request.user, status='waiting')

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
    rounds = LittleBacRounds.objects.filter(game=game)
    
    if players.filter(user=request.user).exists():
        current_round = rounds.last()
        return render(request, 'games/littlebac/game.html', {'game': game, 'players': players, 'round': current_round})
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

    # Récupère le round actuel (dernier round)
    current_round = LittleBacRounds.objects.filter(game=game).last()
    categories = LittleBacCategories.objects.all()
    player = players.get(user=request.user)

    if request.method == "POST":
        print("POST")
        # On vérifie que les réponses commencent par la lettre du round
        round_letter = current_round.letter.upper()
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
                        round=current_round,
                        player=players.get(user=request.user),
                        category=category,
                        answer=answer,
                        is_valid=False
                    )
                    responses.append(response)

            return render(request, 'games/littlebac/finish.html', {
                'responses': responses, 
                'round': current_round, 
                'categories': categories,
                'player': player
            })
        else:
            messages.error(request, "Les réponses doivent commencer par la lettre du tour.")
            return render(request, 'games/littlebac/play.html', {
                'game': game,
                'round': current_round,
                'categories': categories,
                'countdown_remaining': countdown_remaining,
        })

    # Passe les informations du décompte au template
    countdown_remaining = max(
        0, game.countdown_time - int((now() - game.countdown_start_time).total_seconds())
    ) if game.countdown_started else None

    return render(request, 'games/littlebac/play.html', {
        'game': game,
        'round': current_round,
        'categories': categories,
        'countdown_remaining': countdown_remaining,
        'player': player
    })

@login_required()
def game_little_bac_results(request, party_id):
    game = get_object_or_404(LittleBacGames, id=party_id)
    players = LittleBacPlayers.objects.filter(game=game)
    rounds = LittleBacRounds.objects.filter(game=game)
    categories = LittleBacCategories.objects.all()

    all_organized_answers = {}
    scores_by_round = {round.id: {} for round in rounds}
    total_scores = {player.id: 0 for player in players}

    for round in rounds:
        answers = LittleBacAnswers.objects.filter(round=round)

        # On détermine qu'un mot est valide s'il est unique pour une catégorie donnée
        for category in categories:
            valid_answers = answers.filter(category=category).annotate(
                lower_answer=Lower('answer')
            ).values('lower_answer').annotate(
                count=Count('lower_answer')
            ).filter(count=1)
            for answer in valid_answers:
                answers.filter(category=category, answer__iexact=answer['lower_answer']).update(is_valid=True, point=5)

            # Marquer les réponses dupliquées et leur attribuer 1 point
            duplicate_answers = answers.filter(category=category).annotate(
                lower_answer=Lower('answer')
            ).values('lower_answer').annotate(
                count=Count('lower_answer')
            ).filter(count__gt=1)
            for answer in duplicate_answers:
                answers.filter(category=category, answer__iexact=answer['lower_answer']).update(is_valid=False, point=1)

        # Calcule des points pour chaque joueur pour ce round
        for player in players:
            player_score = answers.filter(
                player=player
            ).aggregate(
                total=Sum('point')
            )['total'] or 0
            
            scores_by_round[round.id][player.id] = player_score
            total_scores[player.id] += player_score

    # Organiser les réponses par joueur et par catégorie pour chaque round
    for round in rounds:
        answers = LittleBacAnswers.objects.filter(round=round)
        organized_answers = {}
        for player in players:
            organized_answers[player.id] = {}
            for category in categories:
                answer = answers.filter(player=player, category=category).first()
                if answer:
                    organized_answers[player.id][category.id] = answer.answer
                else:
                    organized_answers[player.id][category.id] = ""
        all_organized_answers[round.id] = organized_answers

    # Mettre à jour les scores totaux des joueurs
    for player in players:
        player.score = total_scores[player.id]
        player.save()

    return render(request, 'games/littlebac/results.html', {
        'game': game,
        'players': players,
        'rounds': rounds,
        'categories': categories,
        'all_organized_answers': all_organized_answers,
        'scores_by_round': scores_by_round,
        'total_scores': total_scores
    })

login_required()
def game_little_bac_start_new_round(request, game_id):
    import random
    import string

    game = LittleBacGames.objects.get(id=game_id)
    if game.author != request.user:
        return redirect('bac_party_games', party_id=game_id)
    
    players = LittleBacPlayers.objects.filter(game=game)

    game.status = 'waiting'
    game.countdown_started = False
    game.countdown_start_time = None
    game.countdown_time = 0
    game.current_phase = "ready_game"
    game.save()

    players.update(is_ready=False, status='playing')

    # Sélectionne une lettre aléatoire pour le nouveau round
    alphabet = string.ascii_uppercase
    letter = random.choice(alphabet)

    # Détermine le numéro du nouveau round
    round_counter = game.rounds.count() + 1

    # Crée un nouveau round
    new_round = LittleBacRounds.objects.create(
        game=game,
        letter=letter,
        round_counter=round_counter
    )

    return redirect('bac_party_games', party_id=game_id)

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