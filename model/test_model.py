import joblib
import numpy as np
import re
import spacy

from sklearn.feature_extraction.text import TfidfVectorizer

# Load the trained model
model = joblib.load("model.joblib")
vectorizer = joblib.load("vectorizer.joblib")

# Test text
test_text = "The AI Dilemma: When Large Language Model Training Reaches A Dead End"

nlp = spacy.load("en_core_web_sm")

# Preprocess the test text
def preprocess_text(txt):
    txt = re.sub('[^a-zA-Z]', ' ', txt)
    txt = txt.lower()
    txt = " ".join(txt.split())

    doc = nlp(txt)

    tokens_filtered = []
    # Iterate through tokens and append to list if it's not a stop word or punctuation mark
    for token in doc:
        if token.is_stop or token.is_punct:
            continue
        tokens_filtered.append(token.lemma_)

    return " ".join(tokens_filtered)

test_processed = np.array([preprocess_text(test_text)])
test = test_processed.reshape(1,-1)

test_vect = vectorizer.transform(test_processed)
res = model.predict(test_vect)

print(res)