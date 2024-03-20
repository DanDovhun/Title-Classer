import pandas as pd
import spacy
import re
import sqlite3

from model import preprocess_text

con = sqlite3.connect("data/dataset.db")
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
    label ITEGER
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