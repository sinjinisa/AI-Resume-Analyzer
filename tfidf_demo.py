
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# STEP 1: Create three example documents
documents = [
    "python sql",
    "python docker",
    "sql excel"
]

# STEP 2: Create the TF-IDF vectorizer
vectorizer = TfidfVectorizer()

# STEP 3: Learn vocabulary and IDF weights
tfidf_matrix = vectorizer.fit_transform(documents)

# STEP 4: Display vocabulary
print("VOCABULARY:")
print(vectorizer.get_feature_names_out())

# STEP 5: Display IDF values
print("\nIDF VALUES:")

for term, weight in zip(
    vectorizer.get_feature_names_out(),
    vectorizer.idf_
):
    print(term, ":", round(weight, 3))

# STEP 6: Display document vectors
print("\nTF-IDF MATRIX:")
print(tfidf_matrix.toarray().round(3))

# STEP 7: Compare documents 1 and 2
similarity = cosine_similarity(
    tfidf_matrix[0],
    tfidf_matrix[1]
)[0, 0]

print("\nCOSINE SIMILARITY:")
print(round(similarity, 3))
