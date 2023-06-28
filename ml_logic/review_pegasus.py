import pandas as pd
import string
import os
# import torch
from transformers import PegasusForConditionalGeneration, PegasusTokenizer, AdamW, T5Tokenizer, T5ForConditionalGeneration
from dbpunctuator.inference import Inference, InferenceArguments
from dbpunctuator.utils import DEFAULT_ENGLISH_TAG_PUNCTUATOR_MAP

# !pip install transformers
# !pip install sentencepiece
# !pip install --upgrade torch transformers pegasus
# !apt-get install -y locales
# !locale-gen en_US.UTF-8
# !update-locale LANG=en_US.UTF-8
# !pip install distilbert-punctuator

#Please note that this is a generated summary and may not capture all the nuances of the original text.

    # def __init__(self):
    #     self.model_name = 'google/pegasus-large'
    #     self.raw_df = None
    #     self.review_df = None
    #     self.pegasus_tokenizer = None
    #     self.pegasus_model = None
    #     self.tokens = None
    #     self.pos_reviews = ''
    #     self.neg_reviews = ''
    #     self.pos_encoded_summary =''
    #     self.neg_encoded_summary =''
    #     # self.device = None


def main(raw_df, hotel_name, pegasus_tokenizer, pegasus_model):
    # raw_df = load_data()
    pos_reviews, neg_reviews = get_reviews(raw_df, hotel_name)
    # pegasus_tokenizer, pegasus_model = load_model()
    pos_encoded_summary, neg_encoded_summary = process_review(pegasus_tokenizer, pegasus_model, pos_reviews, neg_reviews)
    # positive_reviews, negative_reviews = generate_punctuation(pos_encoded_summary, neg_encoded_summary)
    return clean_summary(pos_encoded_summary, neg_encoded_summary)

# def load_data():
#     #pull the data
#     url = os.getcwd() + '/raw_data/cleaned_test_data_5.pkl'
#     raw_df = pd.read_pickle(url)
#     return raw_df

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

def load_model():
    model_name = 'google/pegasus-large'
    pegasus_tokenizer = PegasusTokenizer.from_pretrained(model_name)
    pegasus_model = PegasusForConditionalGeneration.from_pretrained(
        model_name)
    return pegasus_tokenizer, pegasus_model

####Jack added this####
def load_tokenizer():
    model_name = 'google/pegasus-large'
    pegasus_tokenizer = PegasusTokenizer.from_pretrained(model_name)
    return pegasus_tokenizer
####Jack end####

def process_review(pegasus_tokenizer, pegasus_model, pos_reviews, neg_reviews):
    ## positive reviews summary
    tokens = pegasus_tokenizer(pos_reviews, truncation=True, padding='longest', return_tensors='pt')
    encoded_summary = pegasus_model.generate(**tokens, min_length=32, max_length=128, num_return_sequences=1,
                                            decoder_start_token_id=pegasus_tokenizer.pad_token_id)
    pos_encoded_summary = pegasus_tokenizer.decode(encoded_summary.squeeze(), skip_special_tokens=True)

    ## negative reviews summary
    tokens = pegasus_tokenizer(neg_reviews, truncation=True, padding='longest', return_tensors='pt')
    encoded_summary = pegasus_model.generate(**tokens, min_length=32, max_length=128, num_return_sequences=1,
                                            decoder_start_token_id=pegasus_tokenizer.pad_token_id)
    neg_encoded_summary = pegasus_tokenizer.decode(encoded_summary.squeeze(), skip_special_tokens=True)
    return pos_encoded_summary, neg_encoded_summary


def generate_punctuation(pos_encoded_summary, neg_encoded_summary):
    list_pos_summary = [pos_encoded_summary]
    list_neg_summary = [neg_encoded_summary]
    args = InferenceArguments(
    model_name_or_path="Qishuai/distilbert_punctuator_en",
    tokenizer_name="Qishuai/distilbert_punctuator_en",
    tag2punctuator=DEFAULT_ENGLISH_TAG_PUNCTUATOR_MAP)
    punctuator_model = Inference(inference_args=args,
                                verbose=False)
    positive_reviews = punctuator_model.punctuation(list_pos_summary)[0][0]
    negative_reviews = punctuator_model.punctuation(list_neg_summary)[0][0]
    return positive_reviews, negative_reviews

# def generate_punctuation(pos_encoded_summary, neg_encoded_summary):
#     args = InferenceArguments(
#     model_name_or_path="Qishuai/distilbert_punctuator_en",
#     tokenizer_name="Qishuai/distilbert_punctuator_en",
#     tag2punctuator=DEFAULT_ENGLISH_TAG_PUNCTUATOR_MAP)

#     punctuator_model = Inference(inference_args=args,
#                                 verbose=False)

#     positive_reviews = punctuator_model.punctuation(pos_encoded_summary[0])[0][0]
#     negative_reviews = punctuator_model.punctuation(neg_encoded_summary[0])[0][0]
#     return positive_reviews, negative_reviews

def clean_summary(positive_reviews, negative_reviews):
    last_pos_index = positive_reviews.rindex('.')+1
    last_neg_index = negative_reviews.rindex('.')+1
    return positive_reviews[:last_pos_index], negative_reviews[:last_neg_index]
