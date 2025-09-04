def compute_silence_overtalk(df_call):
    intervals=[(float(r.stime), float(r.etime)) for _,r in df_call.iterrows()]
    
    if not intervals: 
        return {'call_duration':0.0,'overtalk_seconds':0.0,'silence_seconds':0.0,'overtalk_pct':0.0,'silence_pct':0.0}
    
    events=[]
    for s,e in intervals:
        events.append((s,1)); events.append((e,-1))
        
    events.sort()
    
    cur=0; last=events[0][0]; overtalk=0.0; speaking=0.0
    for t,delta in events:
        d=t-last
        if cur>0: speaking+=d
        if cur>1: overtalk+=d
        cur+=delta; last=t
        
    start=min(s for s,_ in intervals); end=max(e for _,e in intervals); dur=max(1e-9,end-start)
    
    silence=max(0.0,dur-speaking)
    
    return {'call_duration':dur,'overtalk_seconds':overtalk,'silence_seconds':silence,'overtalk_pct':100.0*overtalk/dur,'silence_pct':100.0*silence/dur}
