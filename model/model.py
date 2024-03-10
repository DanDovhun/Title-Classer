import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize,sent_tokenize
from nltk.stem import PorterStemmer
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import CountVectorizer,TfidfVectorizer
import spacy

def preprocess(txt):
    nlp = spacy.load("en_core_web_sm")

    txt = re.sub('[^a-zA-Z]', ' ', txt)
    txt = txt.lower()
    txt = " ".join(txt.split())

    doc = nlp(txt)
    
    tokens_filtered = []

    for i in doc:
        print(i)
        if i.is_stop or i.is_punct:
            continue

        tokens_filtered.append(i.lemma_)

    return " ".join(tokens_filtered)

plt.rcParams["figure.figsize"] = [10, 5]

df = pd.read_csv('df_file.csv')
df['Text'] = df['Text'].apply(lambda x:x.replace('\n',''))

df['prep_text'] = df['Text'].apply(preprocess)
df.head()