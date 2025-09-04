import pickle
from pathlib import Path
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline

MODEL_DIR = Path(__file__).resolve().parents[2] / 'models'
MODEL_DIR.mkdir(exist_ok=True)

def train_baseline(df, text_col='text', label_col='label', model_name='profanity_baseline'):
    X = df[text_col].fillna('')
    y = df[label_col].astype(int)
    
    pipe = Pipeline([('tfidf', TfidfVectorizer(max_features=20000, ngram_range=(1,2))), ('clf', LogisticRegression(max_iter=1000))])
    
    pipe.fit(X, y)
    out = MODEL_DIR / f"{model_name}.pkl"
    
    with out.open('wb') as f: pickle.dump(pipe, f)
    return out

def load_model(name='profanity_baseline'):
    p = MODEL_DIR / f"{name}.pkl"
    if not p.exists(): raise FileNotFoundError(p)
    with p.open('rb') as f: return pickle.load(f)

def predict_texts(texts, model):
    preds = model.predict(texts)
    probs = model.predict_proba(texts)[:,1] if hasattr(model,'predict_proba') else None
    return preds, probs
