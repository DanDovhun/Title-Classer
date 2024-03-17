import numpy as np
import pandas as pd
import re
import spacy
import joblib

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_val_score

nlp = spacy.load("en_core_web_sm")

def preprocess_text(txt:str):
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

# Load data
df = pd.read_csv('df_file.csv')
df['Text'] = df['Text'].apply(lambda x:x.replace('\n',''))

print("Data loaded")

# Remove duplicates
df.drop_duplicates(ignore_index = True, inplace=True)
print("Duplicates removed, preprocessing data")

# Preprocess text
df['prep_text'] = df['Text'].apply(preprocess_text)
print("Preprocessing done")
vectorizer = TfidfVectorizer(sublinear_tf=True, min_df=5,ngram_range=(1, 2), stop_words='english')
features = vectorizer.fit_transform(df['prep_text']).toarray()

X = features
y = df['Label']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, stratify = y)

print(f'Rows used in training: {len(X_train)}')
print(f'Rows used in evaluation: {len(X_test)}')


training_alg = {'model':LogisticRegression()}
scores = {}

try:
    model = training_alg['model'].fit(X_train, y_train, 
        early_stopping_rounds=10,
        eval_metric='merror',
        eval_set=[(X_test, y_test)])
    
except TypeError:
    model = training_alg['model'].fit(X_train, y_train)
    
training_score = cross_val_score(training_alg['model'], X_train, y_train, cv=5, scoring='accuracy') 
avg_score = round(np.mean(training_score) * 100, 2)

joblib.dump(training_alg["model"], "model.joblib")
joblib.dump(vectorizer, "vectorizer.joblib")

print(training_score)