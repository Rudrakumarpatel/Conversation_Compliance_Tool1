import re
REPEAT_RE = re.compile(r'(.)\1{2,}')

def normalize_text(s: str) -> str:
    if not s: return ''
    s = s.lower()
    
    s = re.sub(r'[^a-z0-9\s@#\$\.\-\/]', ' ', s)
    
    s = REPEAT_RE.sub(lambda m: m.group(1)*2, s)
    
    s = s.replace('0','o').replace('4','a').replace('3','e').replace('1','i').replace('5','s')
    
    return re.sub(r'\s+',' ',s).strip()
