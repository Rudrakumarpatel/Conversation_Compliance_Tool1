import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

# Gemini API KEY
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def classify_texts_with_llm(texts, entity="profanity"):
    """
    Use Gemini to classify a list of texts.
    entity: 'profanity' or 'privacy'
    Returns list of (label, None) tuples.
    """
    model = genai.GenerativeModel("gemini-2.5-flash")
    labels = []

    for text in texts:
        if entity == "privacy":
            prompt = f"""
You are a strict compliance auditor. 
Decide if this text contains **sensitive personal data** or **compliance violations**.

Flag ONLY if it contains:
- Credit card numbers
- SSN or government ID
- Bank details
- Addresses
- Emails
- Phone numbers
- Passwords
- Dates of birth
- HIPAA or medical details

Normal greetings, first names, or company names are SAFE and should NOT be flagged.

Text: "{text}"

Respond ONLY with "1" if it contains sensitive data or violation, otherwise "0".
            """
        else:
            prompt = f"""
You are a strict language filter.
Does this text contain profanity or offensive language?
Text: "{text}"
Respond ONLY "1" if profanity present, else "0".
            """

        try:
            response = model.generate_content(prompt)
            output = response.text.strip()
            label = 1 if "1" in output else 0
            labels.append((label, None))
        except Exception as e:
            print(f"Gemini error: {e}")
            labels.append((0, None))

    return labels
