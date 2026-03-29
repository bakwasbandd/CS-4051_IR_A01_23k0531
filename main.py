from preprocessor import load_stopwords
from indexer import build_indexes, save_indexes, load_indexes
from queryProcessor import process_boolean, process_proximity

SPEECHES_FOLDER = "Speeches"
STOPWORDS_FILE = "Stopword-List.txt"


# build() is our index creator
def build():
    stopwords = load_stopwords(STOPWORDS_FILE)

    # build and save indexes
    inv, pos, doc_mapping = build_indexes(SPEECHES_FOLDER, stopwords)
    save_indexes(inv, pos, doc_mapping) # saving so we dont have to redo it everytime

    # to make sure everything is working! printing stats
    print(f"Done! Indexed {len(doc_mapping)} documents, {len(inv)} unique terms.")


def search():
    inv, pos, doc_mapping = load_indexes() # load the saved indexes

    # making a set of all doc ids (useful for NOT queries)
    all_docs = set(doc_mapping.keys())

    print(f"Loaded {len(doc_mapping)} docs, {len(inv)} terms.")

    while True:
        q = input("\nEnter query (or 'exit' to stop searching): ").strip()

        if q.lower() == "exit":
            break

        # Determine if it's a proximity query (contains "/") or a boolean query
        # Proximity queries are of the form: "term1 term2 /k" (e.g., "freedom speech /3")
        # use positional index for proximity queries, inverted index for boolean queries
        if "/" in q:
            result_ids = process_proximity(q, pos)
        else:
            result_ids = process_boolean(q, inv, all_docs)


        # printing the docs returned by the query processor
        if result_ids:
            print(f"\n{len(result_ids)} document(s) found:")
            for doc_id in sorted(result_ids):
                print(f"  [{doc_id}] {doc_mapping[doc_id]}")
        else:
            print("No documents found.") # nothing returned!


if __name__ == "__main__":
    while True:
        choice = input("\n1. Build the Indexes [Inverted and Positional]\n2. Search\n3. Exit\n\nChoose: ")

        if choice == "1":
            build()
        elif choice == "2":
            search()
        elif choice == "3":
            break
        else:
            print("Invalid choice, Please enter 1, 2, or 3 :(")