import nltk
import pandas as pd
from nltk.corpus import brown

nltk.download('brown')

# NLTK frequencies
freq = nltk.FreqDist(w.lower() for w in brown.words())
nltk_df = pd.DataFrame(freq.most_common(5000), columns=['word', 'frequency'])

# Your custom dataset
your_df = pd.read_csv(r'D:\autocomplete-engine\backend\words.csv')  # rename your current CSV to this

# Merge — your frequencies win on conflict
merged = pd.concat([your_df, nltk_df]).groupby('word')['frequency'].max().reset_index()
merged = merged.sort_values('frequency', ascending=False).reset_index(drop=True)

merged.to_csv('words.csv', index=False)
print(f"Done! Total words: {len(merged)}")