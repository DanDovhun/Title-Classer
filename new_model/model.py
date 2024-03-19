import numpy as np
import pandas as pd
import re
import spacy
import joblib
import sqlite3
import datetime

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_val_score

nlp = spacy.load("en_core_web_sm")

# May not be used directly in training, but is used to preprocessed raw data 
# when transfering them from the csv file to the database
def preprocess_text(txt):
    txt = re.sub('[^a-zA-Z]', ' ', txt) 
    txt = txt.lower()
    txt = " ".join(txt.split()) 
    
    doc = nlp(txt)
    
    tokens_filtered = []
    # Iterate through tokens and append to list if its not stop word or punctuation mark
    for token in doc:
        if token.is_stop or token.is_punct:
            continue
        tokens_filtered.append(token.lemma_)
        
    return " ".join(tokens_filtered)

def train():
    print("Loading data...")
    con = sqlite3.connect("data/dataset.db")
    df = pd.read_sql_query("SELECT * FROM Dataset", con)
    con.close()

    print("Vectorising...")
    vectorizer = TfidfVectorizer(sublinear_tf=True, min_df=5,ngram_range=(1, 2), stop_words='english')
    features = vectorizer.fit_transform(df['prep_text']).toarray()

    print("Training...")

    start = datetime.datetime.now()
    X = features
    y = df["label"]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, stratify = y)

    training_alg = {'model':LogisticRegression()}

    try:
        training_alg['model'].fit(X_train, y_train, 
            early_stopping_rounds=10,
            eval_metric='merror',
            eval_set=[(X_test, y_test)])
            
    except TypeError:
        training_alg['model'].fit(X_train, y_train)

    training_score = cross_val_score(training_alg['model'], X_train, y_train, cv=5, scoring='accuracy') 
    avg_score = round(np.mean(training_score) * 100, 2)

    print(f"\nTraining score: {training_score}")
    print(f"Average score: {avg_score}")

    joblib.dump(training_alg["model"], "saved_model/model.joblib")
    joblib.dump(vectorizer, "saved_model/vectorizer.joblib")
    end = datetime.datetime.now()

    print(f"Training time: {end-start}\n")

if __name__ == "__main__":
    train()

    print("Done")
