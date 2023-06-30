# from dbpunctuator.inference import Inference, InferenceArguments
# from dbpunctuator.utils import DEFAULT_ENGLISH_TAG_PUNCTUATOR_MAP

import pandas as pd
import string
import os
import torch
from transformers import BartTokenizer, BartForConditionalGeneration
import time
import re
# import concurrent.futures

def main(hotel_name):
    raw_df = load_data()
    device = "cuda" if torch.cuda.is_available() else "cpu"
    pos_reviews, neg_reviews = get_reviews(raw_df, hotel_name)
    tokenizer, model = load_bart_model(device)
    pos_encoded_summary, neg_encoded_summary = process_review(tokenizer, model, pos_reviews, neg_reviews)
    # positive_reviews, negative_reviews = generate_punctuation(pos_encoded_summary, neg_encoded_summary)
    return clean_summary(pos_encoded_summary, neg_encoded_summary)


def load_data():
    #pull the data
    url = os.getcwd() + '/raw_data/cleaned_test_data_5.pkl'
    raw_df = pd.read_pickle(url)
    return raw_df

# def define_device(self):
#     self.device = "cuda" if torch.cuda.is_available() else "cpu"

def clean(text):
    if len(text.split()) >= 5:
        text = text.strip()
        text = text.strip('.') +'.'
        return text

def turn_rev_series_to_str(review_series):
    review_str = ''
    rev_length = len(review_series)
    counter = 1
    for item in review_series.values:
        if counter == rev_length:
            review_str += item
        else:
            review_str += item + '\n'
        counter += 1
    return review_str

def get_reviews(raw_df, hotel_name):
    hotel_df = raw_df.query(f'Hotel_Name == "{hotel_name}"')
    positive_reviews = hotel_df['Positive_Review'].dropna().apply(clean).dropna()
    negative_reviews = hotel_df['Negative_Review'].dropna().apply(clean).dropna()
    pos_reviews = turn_rev_series_to_str(positive_reviews)
    neg_reviews = turn_rev_series_to_str(negative_reviews)
    return pos_reviews, neg_reviews

def load_bart_model(device):
    model_name = 'facebook/bart-large'
    bart_tokenizer = BartTokenizer.from_pretrained(model_name)
    bart_model = BartForConditionalGeneration.from_pretrained(model_name).to(device)
    return bart_tokenizer, bart_model

def process_review(bart_tokenizer, bart_model, pos_reviews, neg_reviews, device):
    start_time = time.time()
    # positive reviews summary
    pos_encoded_summary = process_positive_review(bart_tokenizer, bart_model, pos_reviews, device)

    # negative reviews summary
    neg_encoded_summary = process_negative_review(bart_tokenizer, bart_model, neg_reviews, device)

    end_time = time.time()
    print('review process time taken:', end_time - start_time)
    return pos_encoded_summary, neg_encoded_summary

def process_positive_review(bart_tokenizer, bart_model, pos_reviews, device):
    print('start process_positive_review ')
    start_time = time.time()
    tokens = bart_tokenizer(pos_reviews, truncation=True, padding='longest', return_tensors='pt').to(device)
    encoded_summary = bart_model.generate(**tokens, min_length=32, max_length=128,
                                          early_stopping=True, num_return_sequences=1,
                                          decoder_start_token_id=bart_tokenizer.pad_token_id).to(device)
    pos_encoded_summary = bart_tokenizer.decode(encoded_summary.squeeze(), skip_special_tokens=True)
    end_time = time.time()
    print('positive review time taken:', end_time - start_time)
    return pos_encoded_summary

def process_negative_review(bart_tokenizer, bart_model, neg_reviews, device):
    print(' start process_negative_review')
    start_time = time.time()
    tokens = bart_tokenizer(neg_reviews, truncation=True, padding='longest', return_tensors='pt').to(device)
    encoded_summary = bart_model.generate(**tokens, min_length=32, max_length=128,
                                          early_stopping=True, num_return_sequences=1,
                                          decoder_start_token_id=bart_tokenizer.pad_token_id).to(device)
    neg_encoded_summary = bart_tokenizer.decode(encoded_summary.squeeze(), skip_special_tokens=True)
    end_time = time.time()
    print('negative review time taken:', end_time - start_time)
    return neg_encoded_summary

def clean_summary(positive_reviews, negative_reviews):

    #remove the remaining after .
    last_pos_index = positive_reviews.rindex('.')+1
    last_neg_index = negative_reviews.rindex('.')+1

    positive_reviews = positive_reviews[:last_pos_index]
    negative_reviews = negative_reviews[:last_neg_index]

    #remove multiple whitespace
    positive_reviews = re.sub('\s+', ' ', positive_reviews)
    negative_reviews = re.sub('\s+', ' ', negative_reviews)

    #remove multiple .
    positive_reviews = re.sub('\.+', '.', positive_reviews)
    negative_reviews = re.sub('\.+', '.', negative_reviews)

    #capitalize after first letter, full stop and space
    positive_reviews = positive_reviews.lower().capitalize()
    negative_reviews = negative_reviews.lower().capitalize()

    positive_reviews = re.sub('\.\s*([a-z])', lambda x: '. ' + x.group(1).capitalize(), positive_reviews)
    negative_reviews = re.sub('\.\s*([a-z])', lambda x: '. ' + x.group(1).capitalize(), negative_reviews)

    return positive_reviews[:last_pos_index], negative_reviews[:last_neg_index]


# def load_model():
#     model_name = 'google/pegasus-large'
#     pegasus_tokenizer = PegasusTokenizer.from_pretrained(model_name)
#     pegasus_model = PegasusForConditionalGeneration.from_pretrained(
#         model_name)
#     return pegasus_tokenizer, pegasus_model

# def generate_punctuation(pos_encoded_summary, neg_encoded_summary):
#     list_pos_summary = [pos_encoded_summary]
#     list_neg_summary = [neg_encoded_summary]

#     args = InferenceArguments(
#     model_name_or_path="Qishuai/distilbert_punctuator_en",
#     tokenizer_name="Qishuai/distilbert_punctuator_en",
#     tag2punctuator=DEFAULT_ENGLISH_TAG_PUNCTUATOR_MAP)

#     punctuator_model = Inference(inference_args=args,
#                                 verbose=False)

#     positive_reviews = punctuator_model.punctuation(list_pos_summary)[0][0]
#     negative_reviews = punctuator_model.punctuation(list_neg_summary)[0][0]
#     return positive_reviews, negative_reviews

# def process_sequential_review(bart_tokenizer, bart_model, pos_reviews, neg_reviews, device):
#     start_time = time.time()
#     # positive reviews summary
#     pos_encoded_summary = process_positive_review(bart_tokenizer, bart_model, pos_reviews, device)

#     # negative reviews summary
#     neg_encoded_summary = process_negative_review(bart_tokenizer, bart_model, neg_reviews, device)

#     end_time = time.time()
#     print('review process time taken:', end_time - start_time)
#     return pos_encoded_summary, neg_encoded_summary

# def process_concurrent_review(bart_tokenizer, bart_model, pos_reviews, neg_reviews, device):
#     start_time = time.time()

#     with concurrent.futures.ThreadPoolExecutor() as executor:
#         positive_future = executor.submit(process_positive_review, bart_tokenizer, bart_model, pos_reviews, device)
#         negative_future = executor.submit(process_negative_review, bart_tokenizer, bart_model, neg_reviews, device)

#         pos_encoded_summary = positive_future.result()
#         neg_encoded_summary = negative_future.result()

#     ## positive reviews summary
#     # pos_encoded_summary = process_positive_review(bart_tokenizer, bart_model, pos_reviews, device)

#     ## negative reviews summary
#     # neg_encoded_summary = process_negative_review(bart_tokenizer, bart_model, neg_reviews, device)

#     end_time = time.time()
#     print('review process time taken:', end_time - start_time)
#     return pos_encoded_summary, neg_encoded_summary
