document.addEventListener('DOMContentLoaded', () => {
    const container = document.querySelector('.container');
    const gameId = document.querySelector(".container").dataset.gameId;
    const playerId = document.querySelector('#playButton').dataset.playerId;
    const players = document.querySelector('#playersList');
    const playButton = document.querySelector('#playButton');

    const infoNbPlayersReady = document.querySelector('#infoNbPlayersReady');
    const readyCount = document.querySelector('#readyCount');

    let countdownStarted = false;
    let countdownInterval; 
    let countdownIntervalStarted = false;

    /* Fonction pour mettre à jour la liste des joueurs */
    const fetchPlayersList = async () => {
        try {
            const response = await fetch(`/games/api/bac/${gameId}/players`);
            const data = await response.json();

            // Met à jour la liste des joueurs
            players.innerHTML = "";
            data.players.forEach(player => {
                const listItem = document.createElement("li");
                listItem.textContent = `${player.username}`;
                players.appendChild(listItem);
            });

            // Met à jour le nombre de joueurs prêts
            const gameInfo = await fetch(`/games/api/bac/${gameId}/info`);
            const infoData = await gameInfo.json();
            readyCount.textContent = infoData.all_ready;

            // Affiche ou masque les messages en fonction du nombre de joueurs
            playButton.style.display = data.players.length > 1 ? 'block' : 'none';
            document.querySelector('#infoNbPlayersReady').style.display = data.players.length > 1 ? 'block' : 'none';
            document.querySelector('#waitingPlayers').style.display = data.players.length > 1 ? 'none' : 'block';
        } catch (error) {
            console.error("Erreur lors de la récupération des joueurs :", error);
        }
    };

    /* Fonction pour vérifier le décompte */
    const checkCountdownStatus = async () => {
        try {
            const response = await fetch(`/games/api/${gameId}/countdown_status`);
            const data = await response.json();
    
            console.log("Countdown status data:", data); // Vérification
    
            if (data.countdown_started && data.countdown_time > 0) {
                const countdownElement = document.querySelector('#countdown') || document.createElement('p');
                countdownElement.id = 'countdown';
                countdownElement.className = 'countdown';
                countdownElement.innerHTML = `La partie commence dans <strong>${data.countdown_time}</strong> seconde${data.countdown_time > 1 ? 's' : ''}...`;
                container.appendChild(countdownElement);
            }
            
            console.log(data)

            if (data.countdown_started === true && data.countdown_time === 0) {
                clearInterval(countdownInterval); // Arrête l'intervalle
                window.location.href = `/games/bac/party/${gameId}/play`;
            }
        } catch (error) {
            console.error("Erreur lors de la vérification du décompte :", error);
        }
    };

    /* Fonction pour gérer le clic sur le bouton "Prêt" */
    const toggleReadyStatus = async () => {
        try {
            const response = await fetch(`/games/api/bac/${gameId}/player/${playerId}/toggle_ready`);

            if (response.ok) {
                const data = await response.json();
                playButton.textContent = data.is_ready ? "Pas prêt :(" : "Prêt :)";
                playButton.className = data.is_ready ? "btn btn-warning btn-large" : "btn btn-default btn-large";

                // Si tous les joueurs sont prêts et que le décompte n'a pas commencé
                if (data.all_ready === players.childElementCount && !countdownStarted) {
                    countdownStarted = true; // Empêche de redémarrer le décompte
                    const response = await fetch(`/games/api/${gameId}/start_countdown?type=ready_game`);
                    const countdownData = await response.json();

                    if (countdownData.countdown_started) {
                        console.log("Décompte démarré par le serveur.");
                        startCountdownCheck(); // Commence à vérifier le décompte
                    }
                }
            } else {
                console.error("ERREUR API :", response.status);
            }
        } catch (error) {
            console.error("Erreur lors du changement d'état :", error);
        }
    };

    /* Fonction pour démarrer la vérification du décompte */
    const startCountdownCheck = () => {
        if (!countdownIntervalStarted) {
            countdownIntervalStarted = true;
            countdownInterval = setInterval(checkCountdownStatus, 1000);
        }
    };

    /* INITIALISATION */
    playButton.addEventListener('click', toggleReadyStatus);
    fetchPlayersList();
    setInterval(fetchPlayersList, 3000);
    setInterval(checkCountdownStatus, 1000);
});