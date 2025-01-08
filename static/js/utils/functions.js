function openPopup(url) {
    window.open(
        url,
        'PopupWindow',
        'width=400,height=400,scrollbars=no,resizable=no'
    );
}

function copyToClipboard(event) {
    // Récupère le bouton qui a déclenché l'événement
    const button = event.target;

    // Récupère la valeur de l'attribut data-tag
    const tag = button.getAttribute('data-tag');

    // Utilise l'API Clipboard pour copier dans le presse-papiers
    navigator.clipboard.writeText(tag)
}

function modal(id, price) {
    const modal = document.querySelector('.modal');
    if (modal) {
        modal.style.display = 'block';
        const close = document.querySelector('.modal-close');
        const accept = modal.querySelector('#accept');
        accept.innerHTML = `Payer <span class="money">${price}</span>`;
        const decline = modal.querySelector('#decline');

        accept.addEventListener('click', () => {
            window.location.href = `/shop/buy/${id}`;
        });

        decline.addEventListener('click', () => {
            modal.style.display = 'none';
        });

        close.addEventListener('click', () => {
            modal.style.display = 'none';
        });
    }
}

document.addEventListener('DOMContentLoaded', () => {
    const avatars = document.querySelectorAll('.cadre-retro-gameboy');
    avatars.forEach(avatar => {
        console.log("on a trouvé l'avatar");
        const divButtons = document.createElement('div');
        const divCross = document.createElement('div');
        const divStartSelect = document.createElement('div');
        divButtons.classList.add('buttons');
        divCross.classList.add('controls');
        divStartSelect.classList.add('start-select');
        avatar.appendChild(divButtons);
        avatar.appendChild(divCross);
        avatar.appendChild(divStartSelect);
    });
});