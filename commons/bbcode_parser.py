import re

class BBCodeParser:
    def __init__(self):
        # On défini ici les balises BBcode et leur équivalent en html
        self.bbcode_patterns = {
            r'\[b\](.*?)\[/b\]': r'<strong>\1</strong>',
            r'\[i\](.*?)\[/i\]': r'<i>\1</i>',
            r'\[u\](.*?)\[/u\]': r'<underline>\1</underline>',
            r'\[s\](.*?)\[/s\]': r'<strike>\1</strike>',
            r'\[url=(.*?)\](.*?)\[/url\]': r'<a href="\1">\2</a>',
            r'\[url\](.*?)\[/url\]': r'<a href="\1">\1</a>',
            r'\[img alt=(.*?)\](.*?)\[/img\]': r'<img src="\2" alt="\1">',
            r'\[img\](.*?)\[/img\]': r'<img src="\1" alt="Image insérer par un utilisateur">',
        }
    
    def parse(self, text):
        for bbcode, html in self.bbcode_patterns.items():
            text = re.sub(bbcode, html, text, flags=re.DOTALL)
        return text