document.addEventListener('DOMContentLoaded', () => {
    let textarea = document.querySelector('textarea');
    const quoteButtons = document.querySelectorAll('#quote');
    console.log(quoteButtons);
    quoteButtons.forEach((elem) =>{
        const post_id = elem.target;
        elem.addEventListener('click', event => {
            const author = document.querySelector(`#author-post-${post_id}`).textContent;
            const content = document.querySelector(`#post-${post_id}`).textContent;
            
            textarea.value = `[citation=${author}]${content}[/citation]`;
            textarea.focus();
        });
    });

    fetch('/static/js/utils/bbcode-bar.html')
        .then(response => {
            if (response.ok) {
                return response.text();
            } else {
                throw new Error('Impossible de charger le fichier HTML');
            }
        })
        .then(html => {
            textarea.insertAdjacentHTML('beforebegin', html);

            const bbcodeBar = document.querySelector('.bbcode-bar');
            bbcodeBar.addEventListener('click', event => {
                if (event.target.tagName === 'BUTTON' && event.target.classList.contains('bbcode-bar-item')) {
                    const tag = event.target.getAttribute('data-tag');
                    if (tag.includes('][')) {
                        const [openTag, closeTag] = tag.split('][');
                        let startTag = openTag + ']';
                        if(tag === '[list][/list]') {
                            startTag = openTag + '][*]';
                        }
                        const endTag = '[' + closeTag;

                        const startPos = textarea.selectionStart;
                        const endPos = textarea.selectionEnd;

                        const text = textarea.value;

                        textarea.value =
                            text.slice(0, startPos) +
                            startTag +
                            text.slice(startPos, endPos) +
                            endTag +
                            text.slice(endPos);

                        textarea.selectionStart = startPos + startTag.length;
                        textarea.selectionEnd = startPos + startTag.length;

                        textarea.focus();
                    } else {
                        console.error('Format de balise incorrect :', tag);
                    }
                } else if (event.target.tagName === 'BUTTON' && event.target.classList.contains('bbcode-bar-button-gallery')) {
                    let draggableWindows = document.querySelector('.draggable');
                    let header = draggableWindows.querySelector('.header');
                    const contentArea = document.querySelector('.content-gallery')
                    fetch('/gallery/')
                        .then(response => {
                            if(response.ok) {
                                return response.text();
                            } else {
                                throw new Error('Impossible de charger le fichier html de la galerie');
                            }
                        })
                        .then(html => {
                            contentArea.innerHTML = html;
                            draggableWindows.style.display = 'block';
                        })
                        .catch(error => {
                            contentArea.innerHTML = '<h4 style="color:red;">Erreur lors du chargement de la galerie</h4>';
                            draggableWindows.style.display = 'block';
                        })

                    if (draggableWindows) {
                        const windowWidth = window.innerWidth;
                        const windowHeight = window.innerHeight;
                        const modalWidth = draggableWindows.offsetWidth;
                        const modalHeight = draggableWindows.offsetHeight;
                    
                        // Centre la fenêtre au milieu de l'écran
                        draggableWindows.style.left = `${(windowWidth - modalWidth) / 2}px`;
                        draggableWindows.style.top = `${(windowHeight - modalHeight) / 2}px`;
                    
                        // Assure que la fenêtre soit positionnée en mode absolu
                        draggableWindows.style.position = 'fixed';
                    }
                    
                    if (draggableWindows) {
                        if (header) {
                            header.addEventListener('mousedown', (e) => {
                                e.preventDefault();
                                let offsetX = e.clientX - draggableWindows.offsetLeft;
                                let offsetY = e.clientY - draggableWindows.offsetTop;

                                function onMouseMove(e) {
                                    draggableWindows.style.left = e.clientX - offsetX + 'px';
                                    draggableWindows.style.top = e.clientY - offsetY + 'px';
                                }

                                document.addEventListener('mousemove', onMouseMove);

                                document.addEventListener('mouseup', () => {
                                    document.removeEventListener('mousemove', onMouseMove);
                                }, { once: true });
                            });
                        }

                        const closeButton = document.querySelector('#close-window');
                        if (closeButton) {
                            closeButton.addEventListener('click', () => {
                                console.log("test fermeture")
                                draggableWindows.style.display = 'none';
                            });
                        }
                    }
                } else if (event.target.tagName === 'BUTTON' && event.target.classList.contains('bbcode-bar-button-colors')) {
                    console.log('coucou');
                    const colors = [
                        // Basiques
                        'black',
                        'white',
                        
                        // Gris
                        'gray',
                        'darkgray',
                        'silver',
                        
                        // Rouges
                        'red',
                        'darkred',
                        'maroon',
                        'crimson',
                        'coral',
                        
                        // Roses/Violets
                        'pink',
                        'hotpink',
                        'fuchsia',
                        'purple',
                        'blueviolet',
                        'darkmagenta',
                        
                        // Bleus
                        'blue',
                        'navy',
                        'darkblue',
                        'royalblue',
                        'cornflowerblue',
                        'skyblue',
                        'aqua',
                        'cyan',
                        'darkcyan',
                        'teal',
                        
                        // Verts
                        'green',
                        'darkgreen',
                        'lime',
                        'limegreen',
                        'springgreen',
                        'aquamarine',
                        'chartreuse',
                        
                        // Jaunes/Oranges
                        'yellow',
                        'gold',
                        'orange',
                        'darkorange',
                        
                        // Marrons
                        'brown',
                        'chocolate',
                        'saddlebrown',
                        'burlywood',
                        
                        // Tons pastel
                        'aliceblue',
                        'antiquewhite',
                        'azure',
                        'beige',
                        'bisque',
                        'blanchedalmond',
                        'cornsilk',
                        'darkkhaki',
                        'olive'
                    ];

                    const colorButtons = colors.map(color => {
                        const link = document.createElement('a');
                        link.classList.add('bbcode-bar-item-color');
                        link.style.backgroundColor = color;
                        link.style.width = '20px';
                        link.style.height = '20px';
                        link.style.display = 'inline-block';
                        link.style.margin = '2px';
                        link.setAttribute('data-color', color);
                        link.href = '#';
                        return link;
                    });
        
                    const colorBar = document.createElement('div');
                    colorBar.classList.add('bbcode-bar-colors');
                    colorButtons.forEach(link => colorBar.appendChild(link));
        
                    bbcodeBar.appendChild(colorBar);
                } else if (event.target.tagName === 'A' && event.target.classList.contains('bbcode-bar-item-color')) {
                    event.preventDefault();
                    const color = event.target.getAttribute('data-color');
                    if (color) {
                        insertBBCode(`[color=${color}]`, `[/color]`);
                    }
                }
            });
        })
        
        .catch(error => console.error('Erreur: ', error));
});

function insertBBCode(openTag, closeTag) {
    const textarea = document.querySelector('textarea'); // Assurez-vous de sélectionner le bon textarea
    if (!textarea) return;

    const start = textarea.selectionStart;
    const end = textarea.selectionEnd;
    const text = textarea.value;

    const before = text.substring(0, start);
    const selected = text.substring(start, end);
    const after = text.substring(end);

    textarea.value = `${before}${openTag}${selected}${closeTag}${after}`;
    textarea.focus();
    textarea.selectionStart = start + openTag.length;
    textarea.selectionEnd = end + openTag.length;
}

function load_gallery() {
    const contentArea = document.querySelector('.content-gallery')
    fetch('/gallery/')
        .then(response => {
            if(response.ok) {
                return response.text();
            } else {
                throw new Error('Impossible de charger le fichier html de la galerie');
            }
        })
        .then(html => {
            contentArea.innerHTML = html;
            draggableWindows.style.display = 'block';
        })
        .catch(error => {
            contentArea.innerHTML = '<p>Erreur lors du chargement de la galerie</p>';
            draggableWindows.style.display = 'block';
        })
}