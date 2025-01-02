document.addEventListener('DOMContentLoaded', () => {
    const status = document.querySelector('#status');
    /* Fonction pour vérifier le statut de la partie */
    const updateStatus = () => {
        const statuses = {
            waiting: { text: 'En attente', style: 'color:orange;font-style:italic' },
            in_progress: { text: 'En cours', style: 'color:green;font-style:italic' },
            finished: { text: 'Terminée', style: 'color:red;font-style:italic' },
        };

        const currentStatus = statuses[status.textContent];
        if (currentStatus) {
            status.style = currentStatus.style;
            status.textContent = currentStatus.text;
        }
    };
    updateStatus();
})