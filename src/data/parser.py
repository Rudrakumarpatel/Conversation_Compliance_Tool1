import os, json, pandas as pd
from typing import Any, Dict, List

def _find_utterances(obj: Any) -> List[Dict]:
    if isinstance(obj, list):
        return obj
    for key in ('utterances','conversation','transcript','segments','items','results'):
        if isinstance(obj, dict) and key in obj and isinstance(obj[key], list):
            return obj[key]
        
    if isinstance(obj, dict):
        for v in obj.values():
            if isinstance(v, list) and all(isinstance(it, dict) for it in v):
                return v
            
    return []

def _normalize_utt(u: Dict, idx: int) -> Dict:
    text = u.get('text') or u.get('utterance') or u.get('transcript') or u.get('content') or ''
    speaker = u.get('speaker') or u.get('role') or u.get('participant') or 'unknown'
    st_keys = ['stime','start_time','start','start_time_ms','time_start','begin','start_ms']
    et_keys = ['etime','end_time','end','end_time_ms','time_end','finish','end_ms']
    stime = next((u[k] for k in st_keys if k in u), None)
    etime = next((u[k] for k in et_keys if k in u), None)
    
    if stime is None and isinstance(u.get('time'), dict):
        stime = u['time'].get('start') or u['time'].get('stime')
        etime = etime or u['time'].get('end') or u['time'].get('etime')
        
    def _to_float(val):
        try:
            if val is None: return 0.0
            fv = float(val)
            return fv/1000.0 if fv>1e6 else fv
        
        except:
            return 0.0
        
    stime_f = _to_float(stime)
    etime_f = _to_float(etime) if etime is not None else stime_f
    
    return {'call_id': None, 'utterance_id': idx, 'speaker': speaker, 'text': (text or '').strip(),
            'stime': stime_f, 'etime': etime_f, 'duration': max(0.0, etime_f-stime_f)}


def parse_file(path: str) -> pd.DataFrame:
    with open(path,'r',encoding='utf-8') as f:
        data = json.load(f)
    utterances = _find_utterances(data)
    rows = []
    call_id = os.path.splitext(os.path.basename(path))[0]
    
    if not utterances and isinstance(data, dict):
        utterances = [data]
        
    for i,u in enumerate(utterances):
        norm = _normalize_utt(u, i)
        norm['call_id'] = call_id
        rows.append(norm)
        
    df = pd.DataFrame(rows, columns=['call_id','utterance_id','speaker','text','stime','etime','duration'])
    
    if df.empty: return df
    
    return df.sort_values('stime').reset_index(drop=True)

def load_folder(folder: str) -> pd.DataFrame:
    dfs = []
    for fn in sorted(os.listdir(folder)):
        if fn.lower().endswith('.json'):
            p = os.path.join(folder,fn)
            try:
                d = parse_file(p)
                if not d.empty: dfs.append(d)
            except Exception as e:
                print(f"[parse error] {p}: {e}")
                
    if not dfs: return pd.DataFrame(columns=['call_id','utterance_id','speaker','text','stime','etime','duration'])
    
    return pd.concat(dfs, ignore_index=True)
