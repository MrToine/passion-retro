import re

class BBCodeParser:
    def __init__(self):
        # On défini ici les balises BBcode et leur équivalent en html
        self.bbcode_patterns = {
            r'\[b\](.*?)\[/b\]': r'<strong>\1</strong>',
            r'\[i\](.*?)\[/i\]': r'<i>\1</i>',
            r'\[u\](.*?)\[/u\]': r'<u>\1</u>',
            r'\[s\](.*?)\[/s\]': r'<strike>\1</strike>',
            r'\[url=(.*?)\](.*?)\[/url\]': r'<a href="\1">\2</a>',
            r'\[url\](.*?)\[/url\]': r'<a href="\1">\1</a>',
            r'\[url=(.*?)(?:\s+class=(.*?))?\](.*?)\[/url\]': lambda m: f'<a href="{m.group(1)}"{f" class={m.group(2)}" if m.group(2) else ""}>{{m.group(3)}}</a>',
            r'\[url\](?:\s+class=(.*?))?\](.*?)\[/url\]': lambda m: f'<a href="{m.group(2)}"{f" class={m.group(1)}" if m.group(1) else ""}>{{m.group(2)}}</a>',
            r'\[img alt=(.*?)\](.*?)\[/img\]': r'<img src="\2" alt="\1">',
            r'\[img\](.*?)\[/img\]': r'<img src="\1" alt="Image insérer par un utilisateur">',
            r'\[list\](.*?)\[/list\]': r'<ul class="bbcode-list">\1</ul>',
            r'\[\*\](.*?)': r'<li class="bbcode-list">\1</li>',
            r'\[t1\](.*?)\[/t1\]': r'<span style="font-size:2rem;font-weight:800;">\1</span>',
            r'\[t2\](.*?)\[/t2\]': r'<span style="font-size:1.6rem;font-weight:600;">\1</span>',
            r'\[t3\](.*?)\[/t3\]': r'<span style="font-size:1.4rem;font-weight:400;">\1</span>',
            r'\[citation\](.*?)\[/citation\]': r'<fieldset class="quote-bbcode">\1</fieldset>',
            r'\[citation=(.*?)\](.*?)\[/citation\]': r'<fieldset class="quote-bbcode"><legend>\1</legend>\2</fieldset>',
            r'\[color=(.*?)\](.*?)\[/color\]': r'<span style="color: \1;">\2</span>',
            r'\[size=(.*?)\](.*?)\[/size\]': r'<span style="font-size: \1px;">\2</span>',
            r'\[p](.*?)\[/p\]': r'<p>\1</p>',
            r'\[center\](.*?)\[/center\]': r'<div style="text-align:center;">\1</div>',
            r'\[right\](.*?)\[/right\]': r'<div style="text-align:right;">\1</div>',
            r'\[hr\]': r'<hr>',
            
        }
    
    def parse(self, text):
        for bbcode, html in self.bbcode_patterns.items():
            text = re.sub(bbcode, html, text, flags=re.DOTALL)
        return text