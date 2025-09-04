import pandas as pd
from src.detectors.regex_detectors import load_profanity_list, build_profanity_pattern


IN='utterances_all.csv'; OUT='dataset_seed.csv'; 
CHUNKS=20000

def seed_chunk(df, pat):
    df=df.copy()
    df['text']=df['text'].fillna('')
    df['label']=df['text'].apply(lambda t: int(bool(pat.search(str(t).lower()))))
    return df

def main():
    words=load_profanity_list(); pat=build_profanity_pattern(words)
    first=True; total=0
    
    for chunk in pd.read_csv(IN, chunksize=CHUNKS):
        out=seed_chunk(chunk, pat)
        out.to_csv(OUT, index=False, mode='w' if first else 'a', header=first)
        first=False; total+=len(out); print("seeded",total)
        
    print("saved",OUT)
    
if __name__=='__main__':
    main()
