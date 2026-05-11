import nltk
from nltk.stem import PorterStemmer, WordNetLemmatizer
from nltk.tokenize import word_tokenize


def perform_stemming(text):
    """
    Stemming reduces words to their root form by chopping off affixes.
    Example: 'running', 'runs' -> 'run'
    """
    stemmer = PorterStemmer()
    words = word_tokenize(text)
    stemmed_words = [stemmer.stem(word) for word in words]
    return " ".join(stemmed_words)

def perform_lemmatization(text):
    """
    Lemmatization reduces words to their meaningful base form (lemma) using a vocabulary.
    Example: 'better' -> 'good', 'dogs' -> 'dog'
    """
    lemmatizer = WordNetLemmatizer()
    words = word_tokenize(text)
    lemmatized_words = [lemmatizer.lemmatize(word) for word in words]
    return " ".join(lemmatized_words)

if __name__ == "__main__":
    sample_text = "The quick brown foxes are jumping over the lazy dogs and they are playing with their friends in the gardens"
    
    print("--- Original Text ---")
    print(sample_text)
    
    print("\n--- Stemming Result ---")
    print(perform_stemming(sample_text))
    
    print("\n--- Lemmatization Result ---")
    print(perform_lemmatization(sample_text))
