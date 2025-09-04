import os, csv
from src.data.parser import parse_file
INPUT='All_Conversations'; OUT='utterances_all.csv'
def main():
    files = sorted([f for f in os.listdir(INPUT) if f.lower().endswith('.json')])
    if not files: 
        print("No JSON files in",INPUT); return
        
    header=False; written=0
    with open(OUT,'w',encoding='utf-8',newline='') as fout:
        
        writer=None
        for fn in files:
            p=os.path.join(INPUT,fn)
            
            try:
                df=parse_file(p)
                
            except Exception as e:
                print(f"parse error {p}: {e}"); continue
                
            if df.empty: continue
            
            if not header:
                writer=csv.DictWriter(fout, fieldnames=list(df.columns))
                writer.writeheader(); header=True
                
            for _,r in df.iterrows():
                writer.writerow({k:r[k] for k in df.columns})
                written+=1
                
            if written%1000==0: print("written",written)
            
    print("done, written",written,"->",OUT)

if __name__=='__main__': main()
