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
from sklearn.metrics import confusion_matrix, recall_score, precision_score, accuracy_score, f1_score

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
    con = sqlite3.connect("app/model/data/dataset.db")
    df = pd.read_sql_query("SELECT * FROM Dataset ORDER BY label", con)
    con.close()

    print("Vectorising...")
    vectorizer = TfidfVectorizer(sublinear_tf=True, min_df=5,ngram_range=(1, 2), stop_words='english')
    features = vectorizer.fit_transform(df['prep_text']).toarray()

    print("Training...")

    start = datetime.datetime.now()
    X = features
    y = df["label"]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, stratify = y)

    training_alg = {'model':LogisticRegression(multi_class='ovr', C=2)}

    try:
        training_alg['model'].fit(X_train, y_train, 
            early_stopping_rounds=10,
            eval_metric='merror',
            eval_set=[(X_test, y_test)])
            
    except TypeError:
        training_alg['model'].fit(X_train, y_train)
        
    preds = training_alg["model"].predict(X_test)
    score = training_alg["model"].score(X_test, y_test)
    conf_mat = confusion_matrix(y_test, preds)
    
    recall = recall_score(y_test, preds, average="weighted")
    prec = precision_score(y_test, preds, average="weighted")
    acc = accuracy_score(y_test, preds)
    f_one = f1_score(y_test, preds, average="weighted")

    joblib.dump(training_alg["model"], "app/model/saved_model/model.joblib")
    joblib.dump(vectorizer, "app/model/saved_model/vectorizer.joblib")
    training_time = datetime.datetime.now() - start

    print(f"Training time: {training_time}\n")

    return training_time, score, conf_mat, recall, prec, acc, f_one

def add_report(text, label):
    con = sqlite3.connect("app/model/data/dataset.db")
    cur = con.cursor()

    prepped = preprocess_text(text)

    cur.execute("INSERT INTO Dataset VALUES(?, ?, ?)", (text, prepped, label))
    con.commit()

    con.close()

def csv_to_sql():
    con = sqlite3.connect("app/model/data/dataset.db")
    cur = con.cursor()

    # Load data
    df = pd.read_csv('data/df_file.csv')
    df['Text'] = df['Text'].apply(lambda x:x.replace('\n',''))

    df.drop_duplicates(ignore_index = True, inplace=True)

    df['prep_text'] = df['Text'].apply(preprocess_text)
    print("Preprocessing done")

    cur.execute("""
    CREATE TABLE IF NOT EXISTS Dataset(
        text TEXT,
        prep_text TEXT,
        label INTEGER
    )
    """)

    articles = []

    # Arranging a tuple of values to be inserted into the database in this order:
    # unprocessed text, preprocessed text, label
    for index, row in df.iterrows():
        articles.append((row["Text"], row["prep_text"], row["Label"]))

    cur.executemany("INSERT INTO Dataset VALUES(?, ?, ?)", articles)
    con.commit()

    print("Done")
    con.close()

def second_greatest(arr):
    largest = np.max(arr[0])
    index = 0
    second = np.min(arr[0])

    for i in range(0, len(arr[0])):
        if arr[0][i] > second and arr[0][i] < largest:
            index = i

    return index

def classify(text):
    model = joblib.load("app/model/saved_model/model.joblib")
    vectorizer = joblib.load("app/model/saved_model/vectorizer.joblib")
    text = preprocess_text(text)

    reshaped = np.array([text])
    transformed = vectorizer.transform(reshaped)

    prediction = model.predict(transformed)
    probs = model.predict_proba(transformed)

    second = second_greatest(model.predict_proba(transformed))

    print("Hello world")
    print(probs)

    return prediction, second, probs[0][second]

if __name__ == "__main__":
    train()