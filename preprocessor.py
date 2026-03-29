import re
from nltk.stem import PorterStemmer

ps = PorterStemmer()

def load_stopwords(path):
    with open(path) as f:
        return set(word.strip().lower() for word in f)

def preprocess(path, stopwords):
    with open(path, encoding="utf-8", errors="ignore") as f:
        text = f.read().lower()

    words = re.findall(r"[a-z]+", text)

    clean = []
    for pos, w in enumerate(words):
        if w not in stopwords:
            clean.append((ps.stem(w), pos))  # (stemmed_word, original_position)

    return clean