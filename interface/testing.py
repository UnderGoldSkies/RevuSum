import numpy as np
import pandas as pd
import string
import os
import pickle
from nltk.corpus import stopwords
from nltk import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
from sklearn.utils import shuffle
from timeit import default_timer as timer
from ml_logic import params



#Initializing stop_words
stop_words = set(stopwords.words('english')) # you can also choose other languages

#predicting functions
def test_preprocessing(df):
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

    #Apply preprocessing on all sentences in all review
    process_df = basic_preprocessing_data(combined_df)

    #lemmatized all nouns and verbs in sentence in all review
    result_df = lemm_data(process_df)

    #Shuffle dataframe
    shuffle_df = np.random.shuffle(result_df)

    return shuffle_df

#training functions
def combine_and_label(df):

    """
    Combining both positive and negative reviews
    positive label with 1, negative label with 0
    """
    negative_df = pd.DataFrame(df[['Hotel_Name', 'Negative_Review']])
    positive_df = pd.DataFrame(df[['Hotel_Name', 'Positive_Review']])

    #Standardize Column names to review
    negative_df = negative_df.rename(columns={'Negative_Review': 'Review'})
    positive_df = positive_df.rename(columns={'Positive_Review': 'Review'})

    # Get the number of rows in the DataFrame
    num_negative_rows = negative_df.shape[0]
    num_positive_rows = positive_df.shape[0]

    # Create a new column with all 0 and 1 values based on positive/ negative
    negative_df['Label'] = [0] * num_negative_rows
    positive_df['Label'] = [1] * num_positive_rows

    # Concate both
    result = pd.concat([positive_df, negative_df], axis=0)

    # #Split negative and positive columns into two Dataframe
    # negative_df = pd.DataFrame(df.Negative_Review)
    # positive_df = pd.DataFrame(df.Positive_Review)

    # #Standardize Column names to review
    # negative_df = negative_df.rename(columns={'Negative_Review': 'Review'})
    # positive_df = positive_df.rename(columns={'Positive_Review': 'Review'})

    # # Get the number of rows in the DataFrame
    # num_negative_rows = negative_df.shape[0]
    # num_positive_rows = positive_df.shape[0]

    # # Create a new column with all 0 and 1 values based on positive/ negative
    # negative_df['Label'] = [0] * num_negative_rows
    # positive_df['Label'] = [1] * num_positive_rows



    # #Combine both dataframe together to form dataset
    # combined_df = pd.concat([negative_df, positive_df], axis=0,ignore_index=True)

    #Shuffle dataframe
    shuffle_df = shuffle(result)

    return shuffle_df

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
    Applying preprocessing on every sentence in reviews
    """
    df.dropna(subset=['Review'], inplace=True)
    df['Review'] = df['Review'].apply(preprocessing)

    return df

def filter_reviews(df):

    """
    Filtering away reviews with less than 3 words:
    Rationale: Lots of review "No Positive", "No Negative", "None", such
    reviews are not meaningful for keyword sentiment analysis of positive or negative.
    """

    # Apply the filter condition and create a boolean mask
    mask = df['Review'].apply(lambda x: len(x) > 3)

    # Filter the DataFrame based on the mask
    filtered_df = df[mask]

    # Return the filtered DataFrame
    return filtered_df

def lemm_reviews(sentence):

    """
    Lemmatized verb and nouns for words in sentence.
    """

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
    Applying Lemmatized verb and nouns for sentence in all reviews.
    """

    df['Review'] = df['Review'].apply(lemm_reviews)
    df['Review'] = df['Review'].apply(lambda x: ' '.join(x))

    return df


#Deployment prediction functions
def prediction_all_in_one(test_file_path):

    """
    Combine all prediction processing into one
    Input example: '~/code/TechLah/RevuSum/data/testing_df.csv'
    Output example: pred_y and test_y
    """
    start = timer()

    #retrieving csv from filepath
    test_hotelreviews = pd.read_csv(test_file_path)

    end = timer()
    print(f"reading csv = {round(end-start,3)}secs" )

    start = timer()
    #preprocess the test dataframe
    preprocess_df = lemm_data(filter_reviews(basic_preprocessing_data(combine_and_label(test_hotelreviews))))

    end = timer()
    print(f"preprocess dataframe = {round(end-start,3)}secs" )


    start = timer()
    #retrieving model from filepath
    model_file_path = '~/code/TechLah/RevuSum/ML model/hash_nb_model(92%).pkl'
    # Expand the tilde (~) character and get the absolute path
    model_file_path = os.path.expanduser(model_file_path)

    # Load the model from the file
    with open(model_file_path, 'rb') as file:
        hash_nb_model = pickle.load(file)

    end = timer()
    print(f"importing model = {round(end-start,3)}secs" )

    test_X = preprocess_df['Review']
    test_y = preprocess_df['Label']

    start = timer()
    pred_y = hash_nb_model.predict(test_X)

    end = timer()
    print(f"predicting outcome = {round(end-start,3)}secs" )

    return pred_y, test_y


def preprocess_of_test_data(dataframe):

    """
    Split up preprocess
    """
    start = timer()

    # #retrieving csv from filepath
    # test_hotelreviews = pd.read_csv(test_file_path)

    # end = timer()
    # print(f"reading csv = {round(end-start,3)}secs")
    # Replace NaN values with "nothing" in specific columns
    columns_to_replace = ['Positive_Review', 'Negative_Review']

    dataframe[columns_to_replace] = dataframe[columns_to_replace].fillna('nothing')

    start = timer()

    #preprocess the test dataframe
    preprocess_df = lemm_data(filter_reviews(basic_preprocessing_data(combine_and_label(dataframe))))
    end = timer()
    print(f"preprocess dataframe = {round(end-start,3)}secs" )


    return preprocess_df


def prediction_of_test_data(preprocess_df):

    with open(params.SENTIMENT_MODEL_PATH, 'rb') as file:
        hash_nb_model = pickle.load(file)

    #print(f"importing model = {round(end-start,3)}secs" )

    test_X = preprocess_df['Review']
    test_y = preprocess_df['Label']

    pred_y = hash_nb_model.predict(test_X)


    return test_X, pred_y, test_y
