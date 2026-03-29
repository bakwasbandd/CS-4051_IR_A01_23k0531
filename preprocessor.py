import re
from nltk.stem import PorterStemmer

# from nltk's library, PorterStemmer is used to reduce words to their root form (e.g., "running" → "run")
# stemmer object created 
ps = PorterStemmer()

def load_stopwords(path): # gets Stopword-List.txt as input
    with open(path) as f:
        # read stopwords from the file, strip whitespace, convert to lowercase, and return as a set for fast lookup
        return set(word.strip().lower() for word in f)

def preprocess(path, stopwords):
    with open(path, encoding="utf-8", errors="ignore") as f:
        # read the file and convert to lowercase
        text = f.read().lower()

    # extracting only alphabet words (removes numbers, punctuation, etc)
    words = re.findall(r"[a-z]+", text)

    clean = []
    filtered_pos = 0 # position counts only non-stopwords for the positional index
    for w in words:
        if w not in stopwords:
            #  stem the word and add to the clean list along with its position, stopwords not included in this
            clean.append((ps.stem(w), filtered_pos))
            filtered_pos += 1  # position counts only non-stopwords

    return clean