# Technical Report – Conversation Compliance Tool

This technical report summarizes implementation recommendations (Q1 & Q2) and visualization analysis (Q3) for the Conversation Compliance Tool.

---

## Implementation Recommendations (Q1 & Q2)

### Scenario A: Profanity Detection
- **Pattern Matching**:
  - Best for **speed** and **low-complexity deployments**.
  - Easy to maintain (simply extend profanity keyword list).
  - Limited: Fails on creative spellings or new slang.
- **ML Baseline (TF-IDF)**:
  - Best trade-off between **accuracy and cost**.
  - Learns from labeled data to detect profanity beyond static lists.
  - Needs model retraining with new datasets.
- **LLM Prompt System (Gemini)**:
  - Best for **accuracy and nuanced understanding** of context.
  - Handles slang, sarcasm, and complex sentences.
  - Slower and requires API calls; cost increases with dataset size.

**Recommendation**:  
- Use **Pattern Matching** for small deployments and fast screening.  
- Use **ML Baseline** for automated pipelines with limited compute resources.  
- Use **Gemini LLM** for **critical quality assurance** or smaller datasets.

---

### Scenario B: Privacy & Compliance Detection
- **Pattern Matching**:
  - Works well for simple patterns (emails, phone numbers).
  - Prone to **false positives** (names, greetings) and **false negatives** for unusual data formats.
- **LLM Prompt System**:
  - Highly recommended for **compliance-critical industries** (finance, healthcare, legal).
  - Context-aware, reduces false positives, handles global formats.
  - Requires careful prompt engineering to maintain consistency.

**Recommendation**:  
- Combine **Pattern Matching + LLM**: Pattern for quick PII screening, Gemini LLM for final review.  
- Fine-tune Gemini prompts to avoid over-flagging generic names or company introductions.

---

## 2️⃣ Visualization Analysis (Q3)

### Metrics Visualized
1. **Pie Chart**:
   - Shows **overtalk %, silence %, and speaking %** for each call.
   - Helps supervisors see conversation balance at a glance.
2. **Bar Chart (Comparative Analysis)**:
   - Compares **Pattern Matching vs ML TF-IDF models** based on **F1 score, accuracy, precision, recall**.
   - Highlights **which approach is best for profanity detection**.

---

### Insights from Visualizations
| Visualization        | Key Takeaways |
|----------------------|--------------|
| **Call Metrics Pie Chart** | - High silence% -> inefficient calls. <br> - High overtalk% -> poor communication flow. |
| **Comparative Analysis Bar Chart** | - ML models outperform pattern matching for nuanced profanity detection. <br> - LLM not plotted for cost reasons, but recommended for high-stakes use cases. |

---

## 3️⃣ Final Recommendations
| Scenario                 | Recommended Approach                          |
|--------------------------|---------------------------------------------|
| **Profanity Detection**  | ML TF-IDF for automation, LLM for QA.       |
| **Privacy/Compliance**   | Hybrid: Pattern + LLM Prompt System.        |
| **Call Metrics**         | Pattern-based metrics with visualization.   |

---

##  Future Enhancements
-  Fine-tune Gemini on domain-specific datasets.
-  Automate labeling pipeline for ML retraining.
-  Add batch inference for LLM to reduce API cost.
-  Extend analytics with agent performance dashboards.
