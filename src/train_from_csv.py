import pandas as pd, argparse
from src.detectors.ml_detector import train_baseline

def main(csv='dataset_seed.csv'):
    df=pd.read_csv(csv)
    
    if df.empty: 
        raise SystemExit("empty")
    
    if 'text' not in df.columns or 'label' not in df.columns: 
        raise SystemExit("missing cols")
    
    df2=df[['text','label']].dropna(subset=['text'])
    
    path=train_baseline(df2, text_col='text', label_col='label', model_name='profanity_baseline')
    
    print("model ->",path)
    
if __name__=='__main__':
    p=argparse.ArgumentParser(); p.add_argument('--csv',default='dataset_seed.csv'); args=p.parse_args(); main(args.csv)
