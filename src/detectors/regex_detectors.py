import re
from typing import List
from pathlib import Path

BASE = Path(__file__).resolve().parents[2]

def load_profanity_list(path=None)->List[str]:
    p = Path(path) if path else (BASE/'data'/'profanity_list.txt')
    
    if not p.exists(): return []
    
    return [ln.strip().lower() for ln in p.read_text(encoding='utf-8').splitlines() if ln.strip() and not ln.strip().startswith('#')]

def build_profanity_pattern(words:List[str]):
    if not words: return re.compile(r'a^')
    escaped = [re.escape(w) for w in words]
    
    return re.compile(r'\b('+'|'.join(escaped)+r')\b', flags=re.I)

SENSITIVE_PAT = re.compile(r"\b(balance|available balance|amount due|outstanding|account number|acct no|card number|payment due|routing number|bank account)\b|\$\s*\d+|\b\d{6,}\b", flags=re.I)

VERIF_PAT = re.compile(r"\b(date of birth|dob|ssn|social security|last 4|verify|confirm|address|pin|cvv)\b", flags=re.I)

def contains_profanity(text: str, pat=None, wordlist=None)->bool:
    if text is None: return False
    
    t = text.lower()
    
    if pat is None:
        if wordlist is None: wordlist = load_profanity_list()
        pat = build_profanity_pattern(wordlist)
        
    if pat.search(t): return True
    
    cleaned = re.sub(r'[^a-z]','',t)
    
    for w in (wordlist or []):
        if w and w in cleaned: return True
        
    return False

def detect_privacy_violations(df_call):
    violations=[]
    df = df_call.sort_values('stime').reset_index(drop=True)
    for i,row in df.iterrows():
        sp = str(row.speaker).lower()
        text = str(row.text)
        
        if 'agent' in sp:
            if SENSITIVE_PAT.search(text):
                prev = ' '.join(df.loc[max(0,i-6):i-1,'text'].astype(str).tolist())
                if not VERIF_PAT.search(prev):
                    violations.append({'call_id': row.call_id, 'utterance_id': int(row.utterance_id), 'speaker': row.speaker, 'text': row.text, 'stime': row.stime})
                    
    return violations
