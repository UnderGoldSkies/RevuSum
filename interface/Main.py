import numpy as np
import pandas as pd
import string
from nltk.corpus import stopwords
from nltk import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords

def generating_test_train_df(df):
    """
    Generating Demo Day test data from original dataset:
    1) Filter Hotel with 100 reviews or more
    2) Random Sample 50 reviews from each Hotel as Demo Day Test
    3) Keep remainder as Training data
    training_df.shape, testing_df.shape = ((437587, 17), (78151, 17))
    Number of hotels in training and testing = (1074, 1486)
    """

    # Group the Base DataFrame by 'Hotel_Name' and count the number of rows
    grouped_df = df.groupby('Hotel_Name').size().reset_index(name='RowCount')

    # Filter the Base DataFrame to include only hotels with more than 100 rows
    filtered_df = grouped_df[grouped_df['RowCount'] > 100]

    # Hotel_names with less than 100 reviews
    hotelname_morethan_100_reviews=filtered_df.Hotel_Name.to_list()

    # Filter the Base Dataframe to include only Hotel with more than 100 reviews
    hotel_morethan_100_reviews_df = df[df['Hotel_Name'].isin(hotelname_morethan_100_reviews)]

    # Filter the Base DataFrame to get remainder hotels (less than 100 rows)
    remainder_df = df[~df['Hotel_Name'].isin(hotelname_morethan_100_reviews)]

    # Creating a Demo Test Data with 50 samples of each hotel that has more than 100 reviews
    testing_df = hotel_morethan_100_reviews_df.groupby('Hotel_Name', group_keys=False).apply(lambda x: x.sample(50))

    # Get the indices of the rows in 'testing_df'
    indices_to_remove = testing_df.index

    # Creating a Training Data to remove the 50 sampled rows from 'hotel_morethan_100_reviews_df'
    training_df = hotel_morethan_100_reviews_df.drop(indices_to_remove)

    # Combining testing.df with remainder.df (the hotels (less than 100 rows))
    testing_df = pd.concat([testing_df, remainder_df], axis=0,ignore_index=True)

    return training_df, testing_df



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


def preprocessing_keep_stopwords_joined(sentence):
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

    join_list = ' '.join(noun_lemmatized)

    return join_list


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
