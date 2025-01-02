document.addEventListener('DOMContentLoaded', () => {
    const players = document.querySelector('#playersList');
    const gameId = document.querySelector(".container").dataset.gameId;

    const fetchPlayersList = async () => {
        try {
            const response = await fetch(`/games/api/bac/${gameId}/players`);
            const data = await response.json();

            // Met à jour la liste des joueurs
            players.innerHTML = "";
            data.players.forEach(player => {
                const listItem = document.createElement("li");
                const status = player.status === "playing" ? '<i>En train de jouer...</i>' : 'A fini de jouer';
                listItem.textContent = `${player.username} (${status})`;
                players.appendChild(listItem);
            });
        } catch (error) {
            console.error("Erreur lors de la récupération des joueurs :", error);
        }
    };

    fetchPlayersList();
});