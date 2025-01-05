document.addEventListener('DOMContentLoaded', () => {
    const buttonAddResponse = document.querySelector('#add-response')
    const buttonAddAsk = document.querySelector('#add-ask')
    const divResponses = document.querySelector('#responses')
    const divQuestions = document.querySelector('#questions')
    let responses = 0;
    let questions = 0;
    
    if (buttonAddResponse) {
        buttonAddResponse.addEventListener('click', () => {
            // Si on clique sur le bouton, on ajoute un champ de réponse
            responses++;
            const newResponse = document.createElement('div')
            newResponse.classList.add('form-group')
            newResponse.innerHTML = `
                <input type="text" name="response-${responses}" class="form-control" placeholder="Réponse">
            `
            divResponses.appendChild(newResponse)
        })
    }

    if (buttonAddAsk) {
        buttonAddAsk.addEventListener('click', () => {
            // Si on clique sur le bouton, on ajoute un champ de question
            questions++;
            const newAsk = document.createElement('div')
            newAsk.classList.add('form-group')
            newAsk.innerHTML = `
                <input type="text" name="ask-${questions}" class="form-control" style="margin-bottom: 20px;" placeholder="Question">
                <a class="btn btn-default btn-small add-response" data-question="${questions}">Ajouter une réponse</a>
                <div class="responses" id="responses-${questions}"></div>
            `
            divQuestions.appendChild(newAsk)

            const hr = document.createElement('hr');
            hr.style.marginTop = '20px';
            hr.style.marginBottom = '20px';
            divQuestions.appendChild(hr);

            // Add event listener for the new "Ajouter une réponse" button
            newAsk.querySelector('.add-response').addEventListener('click', (event) => {
                const questionId = event.target.getAttribute('data-question');
                const responseContainer = document.querySelector(`#responses-${questionId}`);
                const responseCount = responseContainer.children.length + 1;
                const newResponse = document.createElement('div');
                newResponse.classList.add('form-group');
                newResponse.innerHTML = `
                    <input type="text" name="response-${questionId}-${responseCount}" class="form-control" placeholder="Réponse">
                    <p><label for="is_correct-${questionId}-${responseCount}">Réponse correcte ?</label> <input type="radio" name="is_correct-${questionId}" class="form-check-input" id="is_correct-${questionId}-${responseCount}" value="${responseCount}"></p>
                `;
                responseContainer.appendChild(newResponse);
            });
        })
    }
})