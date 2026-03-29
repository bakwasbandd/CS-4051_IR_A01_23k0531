import re
from nltk.stem import PorterStemmer

ps = PorterStemmer()

def process_word(word):
    word = word.lower()
    word = re.sub(r'[^a-z]', '', word)
    return ps.stem(word)


def process_boolean(query, index, all_docs):
    parts = query.strip().lower().split()

    processed = []
    for p in parts:
        if p not in ("and", "or", "not"):
            processed.append(process_word(p))
        else:
            processed.append(p)

    # Single word
    if len(processed) == 1:
        return index.get(processed[0], set())

    # Two words no operator → implicit AND  [fixes the error for Hillary Clinton]
    if len(processed) == 2 and processed[0] != "not":
        return index.get(processed[0], set()) & index.get(processed[1], set())

    # NOT x
    if len(processed) == 2 and processed[0] == "not":
        return all_docs - index.get(processed[1], set())

    # t1 OP t2
    if len(processed) == 3:
        t1, op, t2 = processed
        s1 = index.get(t1, set())
        s2 = index.get(t2, set())
        if op == "and":
            return s1 & s2
        if op == "or":
            return s1 | s2
        if op == "not":
            return s1 - s2

    # t1 OP t2 OP t3
    if len(processed) == 5:
        t1, op1, t2, op2, t3 = processed
        s1 = index.get(t1, set())
        s2 = index.get(t2, set())
        s3 = index.get(t3, set())

        if op1 == "and":
            temp = s1 & s2
        elif op1 == "or":
            temp = s1 | s2
        elif op1 == "not":
            temp = s1 - s2

        if op2 == "and":
            return temp & s3
        elif op2 == "or":
            return temp | s3
        elif op2 == "not":
            return temp - s3

    return set()


def process_proximity(query, pos_index):
    parts = query.strip().split()

    w1 = process_word(parts[0])
    w2 = process_word(parts[1])
    k = int(parts[3])

    result = set()

    if w1 not in pos_index or w2 not in pos_index:
        return result

    docs1 = pos_index[w1]
    docs2 = pos_index[w2]

    common_docs = set(docs1.keys()) & set(docs2.keys())

    for doc in common_docs:
        found = False
        for p1 in docs1[doc]:
            for p2 in docs2[doc]:
                if abs(p1 - p2) <= k + 1:
                    found = True
                    break
            if found:
                break
        if found:
            result.add(doc)

    return result