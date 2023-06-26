import pandas as pd
import string
import os
import torch
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

class Review_Pegasus:

    def __init__(self):
        self.model_name = 'google/pegasus-large'
        self.raw_df = None
        self.review_df = None
        self.pegasus_tokenizer = None
        self.pegasus_model = None
        self.tokens = None
        self.pos_reviews = ''
        self.neg_reviews = ''
        self.pos_encoded_summary =''
        self.neg_encoded_summary =''
        # self.device = None

    def load_data(self):
        #pull the data
        url = os.getcwd() + '/raw_data/hotel_reviews.csv'
        self.raw_df = pd.read_csv(url)

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

    def get_reviews(self):
        positive_reviews = self.hotel_df['Positive_Review'].apply(self.clean).dropna()
        negative_reviews = self.hotel_df['Negative_Review'].apply(self.clean).dropna()
        self.pos_reviews = self.turn_rev_series_to_str(positive_reviews)
        self.neg_reviews = self.turn_rev_series_to_str(negative_reviews)

    def load_model(self):
        self.pegasus_tokenizer = PegasusTokenizer.from_pretrained(self.model_name)
        self.pegasus_model = PegasusForConditionalGeneration.from_pretrained(
            self.model_name)

    def process_review(self):
        ## positive reviews summary
        tokens = self.pegasus_tokenizer(self.pos_reviews, truncation=True, padding='longest', return_tensors='pt')
        encoded_summary = self.pegasus_model.generate(**tokens, min_length=32, max_length=128, num_return_sequences=1,
                                                decoder_start_token_id=self.pegasus_tokenizer.pad_token_id)
        self.pos_encoded_summary = self.pegasus_tokenizer.decode(encoded_summary.squeeze(), skip_special_tokens=True)

        ## negative reviews summary
        tokens = self.pegasus_tokenizer(self.neg_reviews, truncation=True, padding='longest', return_tensors='pt')
        encoded_summary = self.pegasus_model.generate(**tokens, min_length=32, max_length=128, num_return_sequences=1,
                                                decoder_start_token_id=self.pegasus_tokenizer.pad_token_id)
        self.neg_encoded_summary = self.pegasus_tokenizer.decode(encoded_summary.squeeze(), skip_special_tokens=True)

    def generate_punctuation(self):
        args = InferenceArguments(
        model_name_or_path="Qishuai/distilbert_punctuator_en",
        tokenizer_name="Qishuai/distilbert_punctuator_en",
        tag2punctuator=DEFAULT_ENGLISH_TAG_PUNCTUATOR_MAP)

        punctuator_model = Inference(inference_args=args,
                                    verbose=False)

        positive_reviews = punctuator_model.punctuation(self.pos_encoded_summary)[0][0]
        negative_reviews = punctuator_model.punctuation(self.neg_encoded_summary)[0][0]
        return positive_reviews, negative_reviews
