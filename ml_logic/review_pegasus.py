import pandas as pd
import os
import time
import re
import vertexai
from vertexai.language_models import TextGenerationModel
# !pip install vertexai
# !pip install "shapely<2.0.0"
# !pip install google-cloud-aiplatform >= 1.26.0
# vertexai==0.0.1

def main(df, hotel_name):
    pos_reviews, neg_reviews = get_reviews(df, hotel_name)
    positive_summary, negative_summary = process_review(pos_reviews, neg_reviews)
    return (positive_summary, negative_summary)

def load_data():
    #pull the data

    path = os.getcwd()
    url = os.path.join(path, '..', 'data', 'cleaned_test_data_5.pkl')
    raw_df = pd.read_pickle(url)
    return raw_df

def first_clean(text):
    if len(text.split()) >= 5:
        text = text.strip()
        text = text.strip('.') +'.'
        return text

def turn_rev_series_to_str(review_series):
    review_str = ''
    rev_length = min(249, len(review_series))
    counter = 1
    for item in review_series.values:
        item = clean_text(item)
        if counter == rev_length:
            review_str += item
            break
        else:
            review_str += item + ' '
        counter += 1
    return review_str

def clean_text(text):
    #remove multiple whitespace
    text = re.sub('\s+', ' ', text)

    #remove multiple .
    text = re.sub('\.+', '.', text)

    #capitalize after first letter, full stop and space
    text = text.lower().capitalize()

    text = re.sub('\.\s*([a-z])', lambda x: '. ' + x.group(1).capitalize(), text)
    return text.strip()

def get_reviews(raw_df, hotel_name):
    hotel_df = raw_df.query(f'Hotel_Name == "{hotel_name}"')
    positive_reviews = hotel_df['Positive_Review'].dropna().apply(first_clean).dropna()
    negative_reviews = hotel_df['Negative_Review'].dropna().apply(first_clean).dropna()
    pos_reviews = turn_rev_series_to_str(positive_reviews)
    neg_reviews = turn_rev_series_to_str(negative_reviews)
    return pos_reviews, neg_reviews

def process_review(positive_reviews, negative_reviews):
    start = time.time()
    vertexai.init(project="wagon-bootcamp-389706", location="us-central1")
    parameters = {
        "temperature": 0.5,
        "max_output_tokens": 1024,
        "top_p": 1,
        "top_k": 40
    }
    print('Load bison model')
    model = TextGenerationModel.from_pretrained("text-bison@001")
    print('Start summarizing positive reviews')
    positive_reviews = "Provide a summary with about five sentences for the following article: " + positive_reviews + "\nSummary:"
    positive_response = model.predict(positive_reviews, **parameters)
    print('Start summarizing negative reviews')
    negative_reviews = "Provide a summary with about five sentences for the following article: " + negative_reviews + "\nSummary:"
    negative_response = model.predict(negative_reviews, **parameters)
    end = time.time()
    print(f'process reviews takes {end-start} seconds')
    return positive_response.text, negative_response.text
