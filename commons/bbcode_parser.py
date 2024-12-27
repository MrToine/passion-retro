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
            r'\[url=(.*?)(?:\s+class=(.*?))?\](.*?)\[/url\]': lambda m: f'<a href="{m.group(1)}"{f" class={m.group(2)}" if m.group(2) else ""}>{{m.group(3)}}</a>',
            r'\[url\](?:\s+class=(.*?))?\](.*?)\[/url\]': lambda m: f'<a href="{m.group(2)}"{f" class={m.group(1)}" if m.group(1) else ""}>{{m.group(2)}}</a>',
            r'\[img alt=(.*?)\](.*?)\[/img\]': r'<img src="\2" alt="\1">',
            r'\[img\](.*?)\[/img\]': r'<img src="\1" alt="Image insérer par un utilisateur">',
            r'\[list\](.*?)\[/list\]': r'<ul class="bbcode-list">\1</ul>',
            r'\[\*\](.*?)': r'<li class="bbcode-list">\1</li>',
            r'\[t1\](.*?)\[/t1\]': r'<h1 class="h1-bbcode">\1</h1>',
            r'\[t2\](.*?)\[/t2\]': r'<h2 class="h2-bbcode">\1</h2>',
            r'\[t3\](.*?)\[/t3\]': r'<h3 class="h3-bbcode">\1</h3>',
            r'\[citation\](.*?)\[/citation\]': r'<fieldset class="quote-bbcode">\1</fieldset>',
            r'\[citation=(.*?)\](.*?)\[/citation\]': r'<fieldset class="quote-bbcode"><legend>\1</legend>\2</fieldset>',
        }
    
    def parse(self, text):
        for bbcode, html in self.bbcode_patterns.items():
            text = re.sub(bbcode, html, text, flags=re.DOTALL)
        return text