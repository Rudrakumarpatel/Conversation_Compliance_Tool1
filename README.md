#  Conversation Compliance Tool

A Streamlit-based tool to analyze conversation transcripts for **profanity**, **privacy/compliance violations**, and **call metrics** (silence, overtalk, speaking time).  
Supports multiple approaches:  
-  Pattern Matching  
-  ML Baseline (TF-IDF)  
-  LLM Prompt System (Google Gemini)  

---

##  Features
-  **File Upload**: Supports JSON and YAML call transcripts.
-  **Profanity Detection**: Detects offensive language using patterns, ML, or LLM.
-  **Privacy & Compliance**: Detects PII (SSN, credit cards, phone numbers, emails, addresses, etc.).
-  **Call Metrics**: Measures silence %, overtalk %, and total call duration.
-  **Visualizations**: Pie chart for call metrics and bar chart for model comparison.
-  **Comparative Analysis**: Compares Pattern Matching vs ML Baseline (LLM manual check).
-  **Gemini-Powered LLM**: Fine-tuned privacy/compliance detection.

---

## Project Structure
```
conversation_compliance_tool/
│__data/
|  |__profanity_list.txt
├── src/
│   ├── app/
│   │   └── streamlit_app.py          # Main Streamlit app
│   ├── data/
│   │   └── parser.py                 # Parses JSON/YAML transcripts
│   ├── detectors/
│   │   ├── regex_detectors.py        # Pattern-based profanity & privacy detection
│   │   ├── ml_detector.py            # ML TF-IDF model for profanity detection
│   │   └── llm_detector.py           # Gemini LLM prompt-based detection
│   |__ metrics/
│   |    |__ call_metrics.py           # Silence, overtalk, and call duration metrics
│   |__utils/
|   |      |__ text_preprocess.py
|   |__create_utterance_csv.py
|   |__export_results.py
|   |__seed_labels_from_csv.py
|   |__train_from_csv.py
|__models/
|__call_metrics.csv
|__ dataset_seed.csv
|__ results.csv
|__ utterances_all.csv
|__tmp.csv
|__Technical_Report.md
├── All_conversations/                # Raw conversation JSON files (ignored by Git)
├── requirements.txt                  # Project dependencies
└── README.md                         # Project documentation
```

---

## 🛠️ Installation

### 1. Clone the repo
```bash
git clone https://github.com//conversation_compliance_tool.git
cd conversation_compliance_tool
```

### 2. Create a virtual environment
```bash
python -m venv venv
venv\Scripts\activate          
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

---

## Setup API Keys (Gemini)

1. Get your API key from [Google AI Studio](https://aistudio.google.com/app/apikey).  
2. Create a `.env` file in the project root:
```bash
GOOGLE_API_KEY=your_api_key_here
```

---

## Run the App

### Generate Utterances CSV

```bash
python -m src.create_utterance_csv 
```
### Seed Labels from CSV
```bash
python -m src.seed_labels_from_csv 
```

### Train ML Model
```bash
python -m src.train_from_csv --csv dataset_seed.csv 
```
### Export Analysis Results
```bash
python -m src.export_results --folder All_Conversations --out results.csv
```

### Run Streamlit App
```bash
python -m streamlit run src/app/streamlit_app.py
```

Open the app in your browser: [http://localhost:8501](http://localhost:8501)

---

## How to Use
1. Upload a **JSON/YAML conversation file** (one call per file).  
2. Choose an **Analysis Approach**:
   - Pattern Matching (fast, keyword-based)
   - ML Baseline (TF-IDF model)
   - LLM Prompt System (Gemini-powered)
3. Select an **Entity** to analyze:
   - Profanity Detection
   - Privacy & Compliance
   - Call Metrics
   - Comparative Analysis
4. View flagged utterances, call metrics, or comparison charts.

---

## Example Output
### Profanity Detection
| utterance_id | speaker | text           |
|-------------|---------|----------------|
| 3           | Agent   | This is crap!  |

### Privacy Detection
| utterance_id | speaker | text                            |
|-------------|---------|--------------------------------|
| 6           | Customer| My SSN is 123-45-6789          |

### Call Metrics Pie Chart
Displays silence, overtalk, and speaking time composition.

---

---

## .gitignore Highlights
```
__pycache__/
venv/
.env
models/
All_conversations/
call_metrics.csv
dataset_seed.csv
results.csv
utterances_all.csv
tmp.*
```

---