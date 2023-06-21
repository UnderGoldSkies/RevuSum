import numpy as np
import pandas as pd
import string
from nltk.corpus import stopwords
from nltk import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords



#Initializing stop_words
stop_words = set(stopwords.words('english')) # you can also choose other languages

def preprocessing_remove_stopwords(sentence):
    sentence = sentence.strip("") #whitespace
    sentence = sentence.lower() #lowercase
    sentence = ''.join(char for char in sentence if not char.isdigit()) #remove number
    for punctuation in string.punctuation: #remove punc
        sentence = sentence.replace(punctuation, '')
    word_tokens = word_tokenize(sentence)

    stopwords_removed = [w for w in word_tokens if not w in stop_words]
        # Lemmatizing the verbs
    verb_lemmatized = [
        WordNetLemmatizer().lemmatize(word, pos = "v") # v --> verbs
        for word in stopwords_removed]

    # 2 - Lemmatizing the nouns
    noun_lemmatized = [
        WordNetLemmatizer().lemmatize(word, pos = "n") # n --> nouns
        for word in verb_lemmatized]

    return noun_lemmatized


def preprocessing_keep_stopwords(sentence):
    sentence = sentence.strip("") #whitespace
    sentence = sentence.lower() #lowercase
    sentence = ''.join(char for char in sentence if not char.isdigit()) #remove number
    for punctuation in string.punctuation: #remove punc
        sentence = sentence.replace(punctuation, '')
    word_tokens = word_tokenize(sentence)

        # Lemmatizing the verbs
    verb_lemmatized = [
        WordNetLemmatizer().lemmatize(word, pos = "v") # v --> verbs
        for word in word_tokens]

    # 2 - Lemmatizing the nouns
    noun_lemmatized = [
        WordNetLemmatizer().lemmatize(word, pos = "n") # n --> nouns
        for word in verb_lemmatized]

    return noun_lemmatized


def cleaning(df,preprocess_function):
    #Applying preprocessing on the both positive and negative reviews
    clean_negative_review = []
    cleaned_positive_review = []

    for sentence in df.Negative_Review:
        clean_negative_review.append(preprocess_function(sentence))

    for sentence in df.Positive_Review:
        cleaned_positive_review.append(preprocess_function(sentence))

    clean_negative_df = pd.DataFrame({'Review': clean_negative_review})
    clean_negative_df['Review'] = clean_negative_df['Review'].astype(str)
    clean_positive_df = pd.DataFrame({'Review': cleaned_positive_review})
    clean_positive_df['Review'] = clean_positive_df['Review'].astype(str)

    return clean_negative_df, clean_positive_df


def combine_and_label(clean_negative_df,clean_positive_df):
    # Get the number of rows in the DataFrame
    num_negative_rows = clean_negative_df.shape[0]
    num_positive_rows = clean_positive_df.shape[0]

    # Create a new column with all 0 and 1 values based on positive/ negative
    clean_negative_df['Label'] = [0] * num_negative_rows
    clean_positive_df['Label'] = [1] * num_positive_rows

    clean_negative_df.head(2),clean_positive_df.head(2)
    #Combine both dataframe together to form dataset
    combined_df = pd.concat([clean_negative_df, clean_positive_df], axis=0)

    return combined_df
