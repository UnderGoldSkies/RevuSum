import numpy as np
import pandas as pd
import string
from nltk.corpus import stopwords
from nltk import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords



#Initializing stop_words
stop_words = set(stopwords.words('english')) # you can also choose other languages

#predicting functions


#training functions
def combine_and_label(df):

    """
    Combining both positive and negative reviews
    positive label with 1, negative label with 0
    """

    #Split negative and positive columns into two Dataframe
    negative_df = pd.DataFrame(df.Negative_Review)
    positive_df = pd.DataFrame(df.Positive_Review)

    #Standardize Column names to review
    negative_df = negative_df.rename(columns={'Negative_Review': 'Review'})
    positive_df = positive_df.rename(columns={'Positive_Review': 'Review'})

    # Get the number of rows in the DataFrame
    num_negative_rows = negative_df.shape[0]
    num_positive_rows = positive_df.shape[0]

    # Create a new column with all 0 and 1 values based on positive/ negative
    negative_df['Label'] = [0] * num_negative_rows
    positive_df['Label'] = [1] * num_positive_rows

    #Combine both dataframe together to form dataset
    combined_df = pd.concat([negative_df, positive_df], axis=0,ignore_index=True)

    return combined_df

def preprocessing(sentence):

    """
    Removing whitespace
    Lowercase all words
    Remove digits
    Tokenized Words
    """

    sentence = sentence.strip("") #whitespace
    sentence = sentence.lower() #lowercase
    sentence = ''.join(char for char in sentence if not char.isdigit()) #remove number
    for punctuation in string.punctuation: #remove punc
        sentence = sentence.replace(punctuation, '')
    word_tokens = word_tokenize(sentence)
    return word_tokens

def basic_preprocessing_data(df):

    """
    Applying preprocessing on every review
    """

    df['Review'] = df['Review'].apply(preprocessing)

    return df


def filter_reviews(df):
    # Apply the filter condition and create a boolean mask
    mask = df['Review'].apply(lambda x: len(x) > 3)

    # Filter the DataFrame based on the mask
    filtered_df = df[mask]

    # Return the filtered DataFrame
    return filtered_df

def lemm_reviews(sentence):
    verb_lemmatized = [
        WordNetLemmatizer().lemmatize(word, pos = "v") # v --> verbs
        for word in sentence]

    # 2 - Lemmatizing the nouns
    noun_lemmatized = [
        WordNetLemmatizer().lemmatize(word, pos = "n") # n --> nouns
        for word in verb_lemmatized]

    return noun_lemmatized

def lemm_data(df):

    """
    Applying preprocessing on every review
    """

    df['Review'] = df['Review'].apply(lemm_reviews)

    return df
