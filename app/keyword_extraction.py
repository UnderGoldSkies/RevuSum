import pandas as pd
from nltk.corpus import stopwords
import string
from nltk.stem.wordnet import WordNetLemmatizer
from nltk import word_tokenize, pos_tag

### preprocess the reviews
###
def preprocessing (text):
    for punctuation in string.punctuation:
        text = text.replace(punctuation, ' ') # Remove Punctuation
    lowercased = text.lower() # Lower Case
    tokenized = word_tokenize(lowercased) # Tokenize

    # tag each word with its part of speech
    tagged_words = pos_tag(tokenized)
    # remove adj and adv
    filtered_words = [word for word, tag in tagged_words if tag not in ['JJ', 'JJR', 'JJS', 'RB', 'RBR', 'RBS']]

    words_only = [word for word in filtered_words if word.isalpha()] # Remove numbers
    stop_words = set(stopwords.words('english')) # Make stopword lists
    #add more stop words
    stop_words.update(['hotel', 'booking', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine', 'ten'])
    #print(len(stop_words))

    without_stopwords = [word for word in words_only if not word in stop_words] # Remove Stop Words
    lemma=WordNetLemmatizer() # Initiate Lemmatizer
    lemmatized = [lemma.lemmatize(word) for word in without_stopwords] # Lemmatize
    cleaned = ' '.join(lemmatized) # Join back to a string
    # print(f'{lowercased=}\n', f'{tokenized=}\n', f'{filtered_words=}\n', f'{without_stopwords=}\n', f'{words_only=}\n', f'{lemmatized=}\n', f'{cleaned=}\n')
    # print()
    return cleaned

### test the function ###
# print(preprocessing(cleaned_review_df['Positive_Review'][1]))


# defining a function to preprocess the positive and negative reviews and merge them into one column
# drop those rows with empty processed_text
# return a list of processed_text
def preprocess_all(cleaned_review_df):

    # preporcessing the positive and negative reviews and save them in two new columns:
    cleaned_review_df['pos_processed_text'] = cleaned_review_df.Positive_Review.apply(lambda x: preprocessing(x) if not pd.isna(x) else x)
    cleaned_review_df['neg_processed_text'] = cleaned_review_df.Negative_Review.apply(lambda x: preprocessing(x) if not pd.isna(x) else x)
    df_now = cleaned_review_df.copy()

    # merge the positive and negative reviews into one new column:'processed_text'
    cleaned_review_df['processed_text'] = cleaned_review_df['pos_processed_text'] + cleaned_review_df['neg_processed_text']

    #drop those rows with empty processed_text
    df_now = cleaned_review_df[['processed_text']].dropna()
    doc_list = df_now['processed_text'].tolist()
    return doc_list

### test the function ###
# doc_list = preprocess_all(cleaned_review_df)
# print(doc_list)

###keyword extraction
###
from keybert import KeyBERT
from sentence_transformers import SentenceTransformer

# function to get the keywords from the text using KeyBERT
def keywords_extract(text, top_n=20):
    sentence_model = SentenceTransformer("all-MiniLM-L6-v2")
    kw_model = KeyBERT(model=sentence_model)
    keywords = kw_model.extract_keywords(text, keyphrase_ngram_range=(1, 1), top_n=top_n)

    # flatten the list of list of keywords
    one_list = [item for sublist in keywords for item in sublist]

    # convert the list to a DataFrame
    keyword_df = pd.DataFrame(one_list, columns=['keyword', 'score'])

    # get the top 10 keywords by groupby keyword and get the sum of the score
    top_keywords = keyword_df.groupby('keyword').sum().sort_values(by='score', ascending=False).head(5)

    #get the the keywords list without the number
    return top_keywords.index.tolist()

### test the function ###
# keywords = keywords_extract(doc_list)
# print(keywords)

### get the keywords for one hotel from the pickle file
#defining a function to get the keywords for one hotel from the pickle file
def test_data_keywords_extract(test_data_path, hotel_name):
    # Read the DataFrame from the pickle file, this is cleaned data, so no need to basic clean again
    review_df = pd.read_pickle(test_data_path)
    cleaned_review_df = review_df[review_df['Hotel_Name'] == hotel_name]
    # print(cleaned_review_df.head())
    doc_list = preprocess_all(cleaned_review_df)
    keywords = keywords_extract(doc_list)
    return keywords



### test the function ###
# # get the keywords for one hotel from the pickle file
# # test data pkl file path
# test_data_path = '/Users/zengsheng/code/TechLah/RevuSum/data/cleaned_test_data_5.pkl'
# # one hotel name
# hotel_name = 'ibis Styles Singapore Albert' #'Ibis Budget Singapore Pearl'

# #get the keywords for one hotel from the pickle file
# top_keywords = test_data_keywords_extract(test_data_path, hotel_name)
# print(top_keywords)
