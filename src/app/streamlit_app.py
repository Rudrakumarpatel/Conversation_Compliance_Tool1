import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

from src.data.parser import parse_file
from src.detectors.regex_detectors import (
    load_profanity_list,
    build_profanity_pattern,
    detect_privacy_violations,
)
from src.detectors.ml_detector import load_model, predict_texts
from src.detectors.llm_detector import classify_texts_with_llm
from src.metrics.call_metrics import compute_silence_overtalk

# Streamlit Config
st.set_page_config(page_title="Compliance Tool", layout="wide")
st.title("Conversation Compliance Tool")

#Sidebar Inputs
uploaded = st.file_uploader(
    "Upload a call file (JSON or YAML)", type=["json", "yaml", "yml"]
)
approach = st.selectbox(
    "Approach", ["Pattern Matching", "ML Baseline (TF-IDF)", "LLM Prompt System"]
)
entity = st.selectbox(
    "Entity",
    ["Profanity Detection", "Privacy & Compliance", "Call Metrics", "Comparative Analysis"],
)

#Load ML Model if Needed
model = None
if approach == "ML Baseline (TF-IDF)" or entity == "Comparative Analysis":
    try:
        model = load_model("profanity_baseline")
    except Exception:
        st.warning(
            "ML model not found. Run training (train_from_csv.py) to create models/profanity_baseline.pkl"
        )

# Handle Uploaded File
if uploaded and entity != "Comparative Analysis":
    ext = uploaded.name.split(".")[-1]
    tmp_path = f"tmp.{ext}"
    with open(tmp_path, "wb") as f:
        f.write(uploaded.getbuffer())
    df = parse_file(tmp_path)

    st.subheader("Call: " + str(df.call_id.iloc[0] if not df.empty else "unknown"))

    # Profanity Detection
    if entity == "Profanity Detection":
        texts = df["text"].fillna("").tolist()

        if approach == "Pattern Matching":
            prof = load_profanity_list()
            pat = build_profanity_pattern(prof)
            flagged = df[df["text"].fillna("").str.lower().apply(lambda t: bool(pat.search(t)))]
            if flagged.empty:
                st.success("No profanity detected (Pattern Matching).")
            else:
                st.error(f"Found {len(flagged)} profanity utterance(s)")
                st.table(flagged[["utterance_id", "stime", "etime", "speaker", "text"]])

        elif approach == "ML Baseline (TF-IDF)":
            if model is None:
                st.error("ML model missing.")
            else:
                preds, probs = predict_texts(texts, model)
                df["pred"] = preds
                df["prob"] = probs
                flagged = df[df["pred"] == 1]
                if flagged.empty:
                    st.success("No profanity detected (ML).")
                else:
                    st.error(f"Found {len(flagged)} profanity utterance(s) (ML)")
                    st.table(flagged[["utterance_id", "stime", "etime", "speaker", "text", "prob"]])

        else:  # LLM Prompt System
            with st.spinner("Profanity Detection with LLM... Please wait."):
                results = classify_texts_with_llm(texts, entity="profanity")

            df["pred"] = [r[0] for r in results]
            flagged = df[df["pred"] == 1]
            if flagged.empty:
                st.success("No profanity detected (LLM).")
            else:
                st.error(f"Found {len(flagged)} profanity utterance(s) (LLM)")
                st.table(flagged[["utterance_id", "stime", "etime", "speaker", "text"]])

    # Privacy Detection
    elif entity == "Privacy & Compliance":
        texts = df["text"].fillna("").tolist()
        if approach == "LLM Prompt System":
            with st.spinner("Privacy & Compliance issues with LLM... Please wait."):
                results = classify_texts_with_llm(texts, entity="privacy")
        
            df["pred"] = [r[0] for r in results]
            flagged = df[df["pred"] == 1]
            if flagged.empty:
                st.success("No privacy issues detected (LLM).")
            else:
                st.error(f"Found {len(flagged)} possible privacy issues (LLM)")
                st.table(flagged[["utterance_id", "stime", "etime", "speaker", "text"]])
        else:
            with st.spinner("Running Pattern Matching for privacy issues..."):
                pv = detect_privacy_violations(df)

            if not pv:
                st.success("No privacy issues detected (Pattern Matching).")
            else:
                st.error(f"Found {len(pv)} possible privacy issues")
                st.table(pd.DataFrame(pv))

    # Call Metrics
    else:
        metrics = compute_silence_overtalk(df)
        st.metric("Call duration (s)", f"{metrics['call_duration']:.2f}")
        st.metric("Overtalk %", f"{metrics['overtalk_pct']:.2f}%")
        st.metric("Silence %", f"{metrics['silence_pct']:.2f}%")
        st.write(metrics)

        st.subheader("Call Metrics Visualization")
        labels = ["Overtalk", "Silence", "Speaking"]
        speaking_pct = max(0.0, 100.0 - metrics["overtalk_pct"] - metrics["silence_pct"])
        values = [metrics["overtalk_pct"], metrics["silence_pct"], speaking_pct]

        fig, ax = plt.subplots()
        ax.pie(values, labels=labels, autopct="%1.1f%%", startangle=90)
        ax.set_title("Call Composition")
        st.pyplot(fig)

# Comparative Analysis (Pattern vs ML vs LLM)
elif entity == "Comparative Analysis":
    st.subheader("Comparative Analysis: Pattern vs ML vs LLM")
    try:
        df = pd.read_csv("dataset_seed.csv")
        if "label" not in df.columns:
            st.error("dataset_seed.csv must have 'label' column.")
        else:
            y_true = df["label"]

            # Pattern predictions
            prof = load_profanity_list()
            pat = build_profanity_pattern(prof)
            pattern_preds = df["text"].fillna("").apply(lambda t: int(bool(pat.search(t.lower()))))

            # ML predictions
            ml_preds = None
            if model:
                texts = df["text"].fillna("").tolist()
                ml_preds, _ = predict_texts(texts, model)

            # Metrics
            results = []
            def calc_metrics(name, preds):
                acc = accuracy_score(y_true, preds)
                prec = precision_score(y_true, preds, zero_division=0)
                rec = recall_score(y_true, preds, zero_division=0)
                f1 = f1_score(y_true, preds, zero_division=0)
                return [name, acc, prec, rec, f1]

            results.append(calc_metrics("Pattern Matching", pattern_preds))
            if ml_preds is not None:
                results.append(calc_metrics("ML Baseline", ml_preds))

            st.dataframe(pd.DataFrame(results, columns=["Approach", "Accuracy", "Precision", "Recall", "F1"]))

            # Bar chart
            f1_scores = [r[4] for r in results]
            names = [r[0] for r in results]
            fig, ax = plt.subplots()
            ax.bar(names, f1_scores, color=["blue", "green"])
            ax.set_ylabel("F1 Score")
            ax.set_title("F1 Comparison (Profanity)")
            st.pyplot(fig)

            st.info("LLM can be evaluated manually (expensive to run on full dataset).")
            st.success("Recommendation: Use ML or LLM for nuanced profanity detection. Pattern for privacy & metrics.")

    except FileNotFoundError:
        st.error("dataset_seed.csv not found.")

else:
    st.info("Upload a single-call file or choose Comparative Analysis.")
