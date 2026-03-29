from preprocessor import load_stopwords
from indexer import build_indexes, save_indexes, load_indexes
from queryProcessor import process_boolean, process_proximity

SPEECHES_FOLDER = "Speeches"
STOPWORDS_FILE = "Stopword-List.txt"


def build():
    stopwords = load_stopwords(STOPWORDS_FILE)
    inv, pos, doc_mapping = build_indexes(SPEECHES_FOLDER, stopwords)
    save_indexes(inv, pos, doc_mapping)
    print(f"Done! Indexed {len(doc_mapping)} documents, {len(inv)} unique terms.")


def search():
    inv, pos, doc_mapping = load_indexes()

    all_docs = set(doc_mapping.keys())

    print(f"Loaded {len(doc_mapping)} docs, {len(inv)} terms.")

    while True:
        q = input("\nEnter query (or 'exit'): ").strip()

        if q.lower() == "exit":
            break

        if "/" in q:
            result_ids = process_proximity(q, pos)
        else:
            result_ids = process_boolean(q, inv, all_docs)

        if result_ids:
            print(f"\n{len(result_ids)} document(s) found:")
            for doc_id in sorted(result_ids):
                print(f"  [{doc_id}] {doc_mapping[doc_id]}")
        else:
            print("No documents found.")


if __name__ == "__main__":
    while True:
        choice = input("\n1. Build Index\n2. Search\n3. Exit\nChoose: ")

        if choice == "1":
            build()
        elif choice == "2":
            search()
        elif choice == "3":
            break
        else:
            print("Invalid choice.")