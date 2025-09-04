import argparse, pandas as pd
from src.data.parser import load_folder
from src.detectors.regex_detectors import load_profanity_list, build_profanity_pattern, detect_privacy_violations
from src.metrics.call_metrics import compute_silence_overtalk

def run(folder='All_Conversations', out='results.csv'):
    df = load_folder(folder)
    prof = load_profanity_list(); pat = build_profanity_pattern(prof)
    flagged=[]; calls=[]
    
    for call_id, g in df.groupby('call_id'):
        g = g.sort_values('stime')
        
        for _,r in g.iterrows():
            role = 'agent' if 'agent' in str(r.speaker).lower() else 'borrower'
            if pat.search(str(r.text).lower()):
                flagged.append({'call_id':call_id,'utterance_id':int(r.utterance_id),'speaker':r.speaker,'role':role,'text':r.text,'issue':'profanity'})
                
        pv = detect_privacy_violations(g)
        
        for v in pv: flagged.append({'call_id':call_id,'utterance_id':v['utterance_id'],'speaker':v['speaker'],'role':'agent','text':v['text'],'issue':'privacy'})
        
        metrics = compute_silence_overtalk(g)
        calls.append({'call_id':call_id,'call_duration':metrics['call_duration'],'overtalk_pct':metrics['overtalk_pct'],'silence_pct':metrics['silence_pct']})
        
    pd.DataFrame(flagged).to_csv(out,index=False)
    pd.DataFrame(calls).to_csv('call_metrics.csv',index=False)
    
    print("exported",out,"and call_metrics.csv")

if __name__=='__main__':
    p=argparse.ArgumentParser(); p.add_argument('--folder',default='All_Conversations'); p.add_argument('--out',default='results.csv'); args=p.parse_args(); run(args.folder,args.out)
