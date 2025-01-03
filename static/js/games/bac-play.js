document.addEventListener('DOMContentLoaded', () => {
    const container = document.querySelector('.container');
    const gameId = container.dataset.gameId;
    const players = document.querySelector('#playersList');
    const countdownDisplay = document.querySelector('#countdownDisplay');
    const buttonFinish = document.querySelector('#buttonFinish');
    const playerId = buttonFinish.dataset.playerId;
    const roundId = container.dataset.roundId;
    
    let countdownInterval = null;

    /* Fonction pour récupérer les informations de la partie */
    const fetchGameInfo = async () => {
        try {
            const response = await fetch(`/games/api/bac/${gameId}/info_party`);
            const data = await response.json();

            // Mise à jour de la liste des joueurs
            players.innerHTML = "";
            Object.values(data.players).forEach(player => {
                const listItem = document.createElement("li");
                const status = player.status === "playing" ? '<i>En train de jouer...</i>' : 'A fini de jouer';
                listItem.innerHTML = `${player.username} (${status})`;
                players.appendChild(listItem);
            });

            const allPlayersOvered = data.players.every(player => player.status === "overed");

            // Gestion du décompte
            if (data.countdown_started && data.current_phase === "finish_game") {
                if (!countdownInterval && data.countdown_time > 0) {
                    startCountdown(data.countdown_time);
                    countdownDisplay.style.display = "block"; // Affiche le décompte
                } else if (data.countdown_time <= 0 || allPlayersOvered) {
                    clearInterval(countdownInterval); // Arrête l'intervalle si actif
                    countdownDisplay.style.display = "none"; // Cache le décompte
                    stopGame();
                }
            }

            // On vérifie que le joueur est bien la liste des joueurs et que son status est overed
            console.log(data.players)
            console.log(playerId)
            const player = data.players.find(player => player.username === playerId);
            console.log(player)
            if(player && player.status === "overed") {
                clearInterval(countdownInterval); // Arrête l'intervalle si actif
                countdownDisplay.style.display = "none"; // Cache le décompte
                buttonFinish.style.display = "none"; // Cache le bouton de fin de partie
                document.querySelector('#textFinished').style.display = "block"; // Affiche le message de fin de partie    
                // window.location.href = `/games/bac/party/${gameId}/results`;
            } else {
                console.log('Le joueur n\'a pas terminé la partie');
            }
        } catch (error) {
            console.error("Erreur lors de la récupération des informations de la partie :", error);
        }
    };

    /* Fonction pour démarrer le décompte */
    const startCountdown = (initialTime) => {
        console.log("Démarrage du décompte...");
        let countdownTime = initialTime;

        countdownInterval = setInterval(() => {
            // Affichage du décompte
            console.log(`Temps restant : ${countdownTime} seconde${countdownTime > 1 ? 's' : ''}`);
            countdownTime--;
            countdownDisplay.style.display = "block";
            countdownDisplay.textContent = `Temps restant : ${countdownTime} seconde${countdownTime > 1 ? 's' : ''}`;

            if (countdownTime <= 0) {
                clearInterval(countdownInterval);
                countdownDisplay.style.display = "none"; // Cache le décompte
                buttonFinish.style.display = "none"; // Cache le bouton
                stopGame();
            }
        }, 1000);
    };

    /* Fonction pour gérer la soumission du formulaire */
    const handleFormSubmit = async (form) => {
        try {
            const formData = new FormData(form);
            const response = await fetch(form.action, {
                method: "POST",
                body: formData,
            });

            if (response.ok) {
                console.log("Formulaire soumis avec succès.");
                buttonFinish.style.display = "none"; // Cache le bouton
                document.querySelector('#textFinished').style.display = "block"; // Affiche le message
                
                // Lance le décompte pour tous les joueurs
                const countdownResponse = await startCountdownForAllPlayers();
                if (countdownResponse && countdownResponse.success) {
                    await fetchGameInfo(); // Rafraîchit les informations
                }
            } else {
                console.error("Erreur lors de la soumission du formulaire :", response.status);
            }
        } catch (error) {
            console.error("Erreur réseau lors de la soumission du formulaire :", error);
        }
    };

    /* Fonction pour informer le serveur de démarrer le décompte */
    const startCountdownForAllPlayers = async () => {
        console.log('On appelle l\'API pour lancer le décompte');
        try {
            const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
            const response = await fetch(`/games/api/${gameId}/start_countdown?type=finish_game`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "X-CSRFToken": csrfToken,
                },
                body: JSON.stringify({})
            });

            const data = await response.json();
            if (!response.ok) {
                console.error("Erreur lors du démarrage du décompte :", response.status);
                console.error("Détails de l'erreur:", data);
            }
            return data;
        } catch (error) {
            console.error("Erreur réseau lors du démarrage du décompte :", error);
            return null;
        }
    };

    /* Fonction pour gérer la fin de la partie */
    const stopGame = async () => {
        try {
            const response = await fetch(`/games/api/bac/${gameId}/end_game`);
            
            if (response.ok) {
                console.log('Partie terminée.');
                window.location.href = `/games/bac/party/${gameId}/results`;
            } else {
                console.error("Erreur lors de la fin de la partie :", response.status);
            }
        } catch (error) {
            console.error("Erreur réseau lors de la fin de la partie :", error);
        }
    };

    /* Initialisation */
    const form = document.querySelector('form');
    if (form) {
        form.addEventListener('submit', (e) => {
            e.preventDefault(); // Empêche le rechargement de la page
            handleFormSubmit(form);
        });
    }

    fetchGameInfo();
    setInterval(fetchGameInfo, 3000); // Vérifie les informations toutes les 3 secondes
});
