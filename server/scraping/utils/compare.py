import re
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def preprocess_text(text):
    # Convert to lowercase and remove punctuation
    text = text.lower()
    text = re.sub(r"[^\w\s]", "", text)
    return text


def tokenize_text(text):
    # Tokenize text into individual words
    tokens = text.split()
    return tokens


def remove_stopwords(tokens):
    # Remove stop words
    stop_words = set(stopwords.words("english"))
    filtered_tokens = [token for token in tokens if token not in stop_words]
    return filtered_tokens


def stem_tokens(tokens):
    # Perform stemming
    stemmer = PorterStemmer()
    stemmed_tokens = [stemmer.stem(token) for token in tokens]
    return stemmed_tokens


def calculate_similarity(name1, name2):
    # Preprocess and tokenize the names
    name1 = preprocess_text(name1)
    name2 = preprocess_text(name2)

    tokens1 = tokenize_text(name1)
    tokens2 = tokenize_text(name2)

    # Remove stop words from the tokens
    filtered_tokens1 = remove_stopwords(tokens1)
    filtered_tokens2 = remove_stopwords(tokens2)

    # Perform stemming on the tokens
    stemmed_tokens1 = stem_tokens(filtered_tokens1)
    stemmed_tokens2 = stem_tokens(filtered_tokens2)

    # Convert the token lists to strings
    processed_name1 = " ".join(stemmed_tokens1)
    processed_name2 = " ".join(stemmed_tokens2)

    # Calculate cosine similarity
    tfidf_vectorizer = TfidfVectorizer()
    tfidf_matrix = tfidf_vectorizer.fit_transform([processed_name1, processed_name2])
    similarity = cosine_similarity(tfidf_matrix[0], tfidf_matrix[1])[0][0]

    return similarity


def similarity(name1, name2, threshold=0.8):
    similarity = calculate_similarity(name1, name2)

    if similarity >= threshold:
        print(f"The names '{name1}' and '{name2}' represent the same organization.")
        return True
    else:
        print(f"The names '{name1}' and '{name2}' represent different organizations.")
        return False


if __name__ == "__main__":
    similarity("The University of Texas at Austin", "University of Texas at Austin")
