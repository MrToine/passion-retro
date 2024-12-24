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