#Originally from Jake Version 1.0
#using heapq — Heap queue algorithm
#https://docs.python.org/3/library/heapq.html
#nlargest(n, iterable, key=None) is an inbuilt function of heapq module in Python /
# that returns the n largest elements from a dataset.

import nltk
import pandas as pd
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from collections import defaultdict
from heapq import nlargest
stop_words = set(stopwords.words("english"))
# Convert set to list, remove 'again', and convert back to set
word_list = list(stop_words)
word_list.append('negative')
stop_words = set(word_list)

#import data from a csv file and store in a dataframe
import pandas as pd
df = pd.read_csv('../raw_data/Hotel_Reviews.csv')

# merger two 'Negative_Review', 'Positive_Review' columns and save to a new column 'Reviews'
df['Reviews'] = df['Negative_Review'] + df['Positive_Review']
X_train = df['Reviews']


# Function to preprocess sentences
def preprocess(sentences):
    lemmatizer = WordNetLemmatizer()
    word_frequencies = defaultdict(int)
    for sentence in sentences:
        words = word_tokenize(sentence.lower())
        words = [lemmatizer.lemmatize(word) for word in words if word.isalnum()]
        for word in words:
            if word not in stop_words:
                word_frequencies[word] += 1
    return word_frequencies

# Function to extract keywords using TextRank
def extract_keywords(sentences, num_keywords=100):
    word_frequencies = preprocess(sentences)
    # Calculate weighted word frequencies
    max_frequency = max(word_frequencies.values())
    for word in word_frequencies.keys():
        word_frequencies[word] = word_frequencies[word] / max_frequency
    # Get top N keywords with highest scores
    top_keywords = nlargest(num_keywords, word_frequencies, key=word_frequencies.get)
    return top_keywords

# Extract keywords from the list of sentences
keywords = extract_keywords(X_train)
