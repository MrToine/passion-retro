const selectPostType = document.querySelector('#post_type');
if (selectPostType) {
    let postsList = [];
    let divChildForm = null;
    const container = document.querySelector('form');
    const buttonSubmit = document.querySelector('#submit-button');
    const divSubmit = document.querySelector('#submit');
    const addPostButton = document.createElement('a');
    
    addPostButton.className = 'btn btn-add';
    addPostButton.textContent = "Ajouter un article";

    selectPostType.addEventListener('change', (event) => {
        const selectedValue = event.target.value;

        if (selectedValue === 'solo') {
            // Supprime le bouton si présent
            buttonSubmit.textContent = 'Créer';
            if (divSubmit.contains(addPostButton)) {
                divSubmit.removeChild(addPostButton);
            }

            // Supprime le conteneur des articles, s'il existe
            if (divChildForm) {
                container.removeChild(divChildForm);
                divChildForm = null; // Réinitialise pour éviter des doublons
            }
        } else if (selectedValue === 'multiple') {
            // Crée le conteneur des articles si non encore créé
            buttonSubmit.textContent = 'Créer mon ensemble d\'articles';
            if (!divChildForm) {
                const hiddenForm = document.createElement('input');
                hiddenForm.type = 'hidden';
                hiddenForm.name = 'type_form';
                hiddenForm.value = 'multiple';
                container.appendChild(hiddenForm);

                divChildForm = document.createElement('div');
                container.appendChild(divChildForm);
            }

            // Ajoute le bouton si non encore ajouté
            if (!divSubmit.contains(addPostButton)) {
                divSubmit.appendChild(addPostButton);
            }

            // Évite les doublons d'écouteurs avec "onclick"
            addPostButton.onclick = () => {
                // Ajoute un numéro d'article à la liste
                const articleNumber = postsList.length + 1;
                postsList.push(articleNumber);

                // Crée un titre pour l'article
                const title = document.createElement('h3');
                title.textContent = `Article enfant #${articleNumber}`;

                const form = document.createElement('form');
                form.method = "POST";
                form.action = "";

                const formTitle = document.createElement('input');
                formTitle.type = 'text';
                formTitle.name = `title-post-${articleNumber}`;
                formTitle.placeholder = `Titre article #${articleNumber}`;
                formTitle.required = true;

                const formContent = document.createElement('textarea');
                formContent.name = `content-post-${articleNumber}`;
                formContent.placeholder = `Contenu article #${articleNumber}`;
                formContent.rows = 10;
                formContent.cols = 40;
                formContent.required = true;

                const formPostType = document.createElement('input');
                formPostType.type = 'hidden';
                formPostType.name = `post-type-${articleNumber}`;
                formPostType.value = 'child';

                divChildForm.appendChild(title);
                // divChildForm.appendChild(form);
                divChildForm.appendChild(formTitle);
                divChildForm.appendChild(formContent);
                divChildForm.appendChild(formPostType);
            };
        }
    });
}