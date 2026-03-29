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
    filtered_pos = 0
    for w in words:
        if w not in stopwords:
            clean.append((ps.stem(w), filtered_pos))
            filtered_pos += 1  # position counts only non-stopwords

    return clean