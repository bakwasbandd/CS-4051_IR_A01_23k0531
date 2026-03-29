import re
from nltk.stem import PorterStemmer

# query has to be preprocessed in the same way as the documents (lowercase, remove punctuation, stem) to ensure matching with the indexes
ps = PorterStemmer()

def process_word(word):
    word = word.lower() # lowercase 
    word = re.sub(r'[^a-z]', '', word) # remove non-alphabetic characters
    return ps.stem(word)  # stem the word to its root 

#### boolean query processor supporting AND, OR, NOT, and parentheses 
def process_boolean(query, index, all_docs):
    query = query.strip() # removes any leading and trailing whitespace

    # Handle NOT (t1 OP t2 ...)
    not_paren = re.match(r'^NOT\s*\((.+)\)$', query, re.IGNORECASE) # matches queries of the form "NOT (t1 OP t2 ...)"
    # if it matches, we process the inner part of the parentheses and then take the complement with respect to all_docs to get the NOT result
    if not_paren:
        inner = not_paren.group(1).strip() # get the inner part of the parentheses and strip whitespace
        inner_result = process_boolean(inner, index, all_docs) # recursively process the inner boolean query
        return all_docs - inner_result # return the set of all documents that are NOT in the inner result

    # Handle t1 OP (t2 OP t3 ...)
    # matches queries of the form "t1 AND (t2 OR t3)", "t1 OR (t2 AND t3)", etc.
    term_paren = re.match(r'^(\w+)\s+(AND|OR|NOT)\s*\((.+)\)$', query, re.IGNORECASE)
    if term_paren:
        t1 = process_word(term_paren.group(1)) # process the first term (before the operator and parentheses)
        op = term_paren.group(2).lower() # get the operator (AND, OR, NOT) and convert to lowercase for consistency
        inner = term_paren.group(3).strip() # get the inner part of the parentheses and strip whitespace
        s1 = index.get(t1, set()) # set of documents for t1 from the index, default to empty set if t1 is not in the index
        inner_result = process_boolean(inner, index, all_docs) # recursively process the inner boolean query
    
        # combine the results based on the operator
        if op == "and":
            return s1 & inner_result
        if op == "or":
            return s1 | inner_result
        if op == "not":
            return s1 - inner_result

    # For simpler queries without parentheses, we split the query into parts and process them based on the operators!!
    parts = query.strip().lower().split()

    processed = []

    # process each part of the query, if it's an operator we keep it as is, if it's a term we preprocess it to match the index(stemming and cleaning)
    for p in parts:
        if p not in ("and", "or", "not"):
            processed.append(process_word(p))
        else:
            processed.append(p)

    # Single word
    if len(processed) == 1:
        return index.get(processed[0], set())

    # Two words no operator → implicit AND
    # e.g., "freedom speech" is treated as "freedom AND speech"
    if len(processed) == 2 and processed[0] != "not":
        return index.get(processed[0], set()) & index.get(processed[1], set())

    # NOT x
    if len(processed) == 2 and processed[0] == "not":
        return all_docs - index.get(processed[1], set()) # return all documents that do not contain the term

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
    # handles queries with two operators and three terms
    if len(processed) == 5:
        t1, op1, t2, op2, t3 = processed
        s1 = index.get(t1, set())
        s2 = index.get(t2, set())
        s3 = index.get(t3, set())

        # combine t1 and t2 based on op1, then combine the result with t3 based on op2
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

#### proximity query processor 
# for queries of the form "term1 term2 /k" where we want to find documents where term1 and term2 appear within k words of each other
def process_proximity(query, pos_index):
    parts = query.strip().split() 
    # query will be split into 4 parts! 
    w1 = process_word(parts[0])
    w2 = process_word(parts[1])
    k = int(parts[3])

    result = set() 

    # if either term is not in the positional index, we can return an empty result immediately since we won't find any documents that satisfy the proximity condition
    if w1 not in pos_index or w2 not in pos_index:
        return result

    docs1 = pos_index[w1]
    docs2 = pos_index[w2]

# intersection of documents that contain both terms
    common_docs = set(docs1.keys()) & set(docs2.keys())

    for doc in common_docs:
        found = False
        for p1 in docs1[doc]:
            for p2 in docs2[doc]:
                if abs(p1 - p2) <= k + 1: # check if the positions of the two terms are within k words of each other (k+1 because positions are 0-indexed)
                    found = True
                    break
            if found:
                break
        if found:
            result.add(doc)

    return result