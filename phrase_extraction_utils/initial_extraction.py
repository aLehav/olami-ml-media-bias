# your_script.py

import pandas as pd
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from collections import Counter
import re

# Download NLTK resources
nltk.download('punkt')
nltk.download('stopwords')

def preprocess_text(text):
    text = text.lower()
    text = re.sub(r'\W', ' ', text)
    tokens = word_tokenize(text)
    tokens = [token for token in tokens if token.isalpha()]
    tokens = [token for token in tokens if token not in stopwords.words('english')]
    return tokens

def get_common_phrases(file_path):
    df = pd.read_csv(file_path)
    articles = df['content'].astype(str).tolist()
    
    all_tokens = [preprocess_text(article) for article in articles]
    all_tokens_flat = [token for sublist in all_tokens for token in sublist]

    common_phrases_counter = Counter(all_tokens_flat)
    common_phrases = [phrase for phrase, _ in common_phrases_counter.most_common(100000)]

    return common_phrases
