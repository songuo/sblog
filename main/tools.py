from unicodedata import normalize
import re


no_meaning = ("a", "an", "the", "of", "and", "at",
              "in", "for", "on", "from", 'to', "by",
              'with', 'as', 'but', 'is', 'are',
              'was', 'were', 'or')
def slugify(text, encoding=None,
         deleted_chars = r'`~!@#$%^&(){}[]=+/\|*?.,'):
    if isinstance(text, str):
        text = text.decode(encoding or 'utf8')
    
    text = re.sub('[`~!@#\$%\^&\(\)\{\}\[\]=\+/\\\|\*\?\.,\t]', '', text)
    clean_text = text.strip().replace(' ', '-').lower()
    clean_text = re.sub('-{2,}', '-', clean_text).strip()
    if '-' in clean_text:
        for d in no_meaning:
            if '-' + d + '-' in clean_text:
                clean_text = clean_text.replace(d + '-', '')

        i = clean_text.find('-')
        if i != -1 and clean_text[:i] in no_meaning:
            clean_text = clean_text[i + 1:]
        
        i = clean_text.rfind('-')
        if i != -1 and clean_text[i + 1:] in no_meaning:
            clean_text = clean_text[:i]
        
    slug = normalize('NFKD', clean_text).encode('utf8', 'ignore')
    return slug

def extract_excerpt(html):
    html = re.sub('</?[a-zA-Z0-9]+>', ' ', html[:300])
    html = re.sub('[ \t\n]+', ' ', html)[:120] + '...'
    return html
