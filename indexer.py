import os
import pickle
from preprocessor import preprocess

def build_indexes(folder, stopwords):
    # inverted index: word -> set of doc_ids
    inverted_index = {}

    # positional index: word -> {doc_id: [positions]}
    positional_index = {}

    # doc_mapping: doc_id -> filename
    # mapping of doc ids to their filenames for easy retrieval during search results
    doc_mapping = {}

    files = sorted(os.listdir(folder))  # sorted for consistency

    for doc_id, filename in enumerate(files):
        if not filename.endswith('.txt'): # skip non-text files if any
            continue

        path = os.path.join(folder, filename)
        doc_mapping[doc_id] = filename

        tokens = preprocess(path, stopwords)  # list of (word, pos)

        for word, pos in tokens:

            # Inverted index
            if word not in inverted_index:
                inverted_index[word] = set() # create a new set for this word if it doesn't exist already
            inverted_index[word].add(doc_id) # add the current doc_id to the set of documents for this word

            # Positional index
            if word not in positional_index:
                positional_index[word] = {}
            if doc_id not in positional_index[word]:
                positional_index[word][doc_id] = []
            positional_index[word][doc_id].append(pos) # add the position of the word in the document to index

    return inverted_index, positional_index, doc_mapping

# save and load functions for the indexes using pickle
# rewrites the files if we run build() again
def save_indexes(inv, pos, doc_mapping):
    with open("inverted_index.pkl", "wb") as f:
        pickle.dump(inv, f)
    with open("positional_index.pkl", "wb") as f:
        pickle.dump(pos, f)
    with open("doc_mapping.pkl", "wb") as f:
        pickle.dump(doc_mapping, f)
    print("Indexes saved successfully.")


def load_indexes():
    with open("inverted_index.pkl", "rb") as f:
        inv = pickle.load(f)
    with open("positional_index.pkl", "rb") as f:
        pos = pickle.load(f)
    with open("doc_mapping.pkl", "rb") as f:
        doc_mapping = pickle.load(f)
    return inv, pos, doc_mapping