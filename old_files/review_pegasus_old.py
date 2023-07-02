import pandas as pd
import string
import os
import torch
import time
import re
from ml_logic import params
import vertexai
from vertexai.language_models import TextGenerationModel

# !pip install transformers
# !pip install sentencepiece
# !pip install --upgrade torch transformers pegasus
# !apt-get install -y locales
# !locale-gen en_US.UTF-8
# !update-locale LANG=en_US.UTF-8
# !pip install distilbert-punctuator


def main(hotel_name):
    raw_df = load_data()
    pos_reviews, neg_reviews = get_reviews(raw_df, hotel_name)
    pos_encoded_summary, neg_encoded_summary = process_review(pos_reviews, neg_reviews)
    # positive_reviews, negative_reviews = generate_punctuation(pos_encoded_summary, neg_encoded_summary)
    # positive_reviews, negative_reviews = clean_summary(pos_encoded_summary, neg_encoded_summary)

    # return clean_summary(positive_reviews, negative_reviews)
    return pos_encoded_summary, neg_encoded_summary

def load_data():
    #pull the data
    path = os.getcwd()
    url = os.path.join(path, '..', 'data', 'cleaned_test_data_5.pkl')
    raw_df = pd.read_pickle(url)
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = params.GOOGLE_CREDENTIAL_PATH
    return raw_df

def define_device(self):
    self.device = "cuda" if torch.cuda.is_available() else "cpu"

def clean(text):
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

def get_reviews(raw_df, hotel_name):

    start = time.time()

    hotel_df = raw_df.query(f'Hotel_Name == "{hotel_name}"')
    positive_reviews = hotel_df['Positive_Review'].dropna().apply(clean).dropna()
    negative_reviews = hotel_df['Negative_Review'].dropna().apply(clean).dropna()
    pos_reviews = turn_rev_series_to_str(positive_reviews)
    neg_reviews = turn_rev_series_to_str(negative_reviews)

    end = time.time()
    print(f"get_reviews = {round(end-start,3)}secs" )
    print("get_reviews ✅")
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
    print('abc')
    model = TextGenerationModel.from_pretrained("text-bison@001")
    print('111')
    positive_reviews = "Provide a summary with about five sentences for the following article: " + positive_reviews + "\nSummary:"
    positive_response = model.predict(positive_reviews, **parameters)
    print('222')
    negative_reviews = "Provide a summary with about five sentences for the following article: " + negative_reviews + "\nSummary:"
    negative_response = model.predict(negative_reviews, **parameters)
    print('333')
    end = time.time()
    print(f'process reviews takes {end-start} seconds')
    return positive_response.text, negative_response.text

# def generate_punctuation(pos_encoded_summary, neg_encoded_summary):
#     list_pos_summary = [pos_encoded_summary]
#     list_neg_summary = [neg_encoded_summary]

#     start = time.time()
#     args = InferenceArguments(
#     model_name_or_path="Qishuai/distilbert_punctuator_en",
#     tokenizer_name="Qishuai/distilbert_punctuator_en",
#     tag2punctuator=DEFAULT_ENGLISH_TAG_PUNCTUATOR_MAP)
#     end = time.time()
#     print(f"tokenizer = {round(end-start,3)}secs" )

#     start = time.time()
#     punctuator_model = Inference(inference_args=args,
#                                 verbose=False)
#     end = time.time()
#     print(f"punctuator_model = {round(end-start,3)}secs" )

#     start = time.time()
#     positive_reviews = punctuator_model.punctuation(list_pos_summary)[0][0]
#     negative_reviews = punctuator_model.punctuation(list_neg_summary)[0][0]
#     end = time.time()
#     print(f"punctuator_model.punctuation = {round(end-start,3)}secs" )
#     print("generate_punctuation ✅")
#     return positive_reviews, negative_reviews

def clean_text(text):
    #remove multiple whitespace
    text = re.sub('\s+', ' ', text)

    #remove multiple .
    text = re.sub('\.+', '.', text)

    #capitalize after first letter, full stop and space
    text = text.lower().capitalize()

    text = re.sub('\.\s*([a-z])', lambda x: '. ' + x.group(1).capitalize(), text)
    return text.strip()

def clean_summary(positive_summary, negative_summary):
    #remove the remaining after .
    last_pos_index = positive_summary.rindex('.')+1
    last_neg_index = negative_summary.rindex('.')+1

    positive_summary = positive_summary[:last_pos_index]
    negative_summary = negative_summary[:last_neg_index]

    positive_summary = clean_text(positive_summary)
    negative_summary = clean_text(negative_summary)
    return positive_summary, negative_summary


#jack's clean summary
# def clean_summary(positive_reviews, negative_reviews):

#     start = time.time()
#     # # Remove ?
#     # positive_reviews = re.sub(r'[?,&]', '', positive_reviews)
#     # negative_reviews = re.sub(r'[?,&]', '', negative_reviews)

#     # # Remove additional spaces
#     # positive_reviews = re.sub(r'\s+', ' ', positive_reviews)
#     # negative_reviews = re.sub(r'\s+', ' ', negative_reviews)

#     # Lower capital everything and capitalize first letter in string
#     positive_reviews = positive_reviews.lower().capitalize()
#     negative_reviews= negative_reviews.lower().capitalize()

#     # Capitalize the first letter after every period
#     positive_reviews = re.sub(r'\.\s?(\w)', lambda m: '. ' + m.group(1).upper(), positive_reviews)
#     negative_reviews = re.sub(r'\.\s?(\w)', lambda m: '. ' + m.group(1).upper(), negative_reviews)

#     last_pos_index = positive_reviews.rindex('.')+1
#     last_neg_index = negative_reviews.rindex('.')+1
#     end = time.time()
#     print(f"clean_summary = {round(end-start,3)}secs" )
#     print("clean_summary ✅")
#     return positive_reviews[:last_pos_index], negative_reviews[:last_neg_index]


# def load_model():
#     model_name = 'google/pegasus-large'
#     pegasus_tokenizer = PegasusTokenizer.from_pretrained(model_name)
#     pegasus_model = PegasusForConditionalGeneration.from_pretrained(
#         model_name)
#     return pegasus_tokenizer, pegasus_model

# ####Jack added this####
# def load_tokenizer():
#     model_name = 'google/pegasus-large'
#     pegasus_tokenizer = PegasusTokenizer.from_pretrained(model_name)
#     return pegasus_tokenizer
# ####Jack end####

# def process_review(pegasus_tokenizer, pegasus_model, pos_reviews, neg_reviews):

#     ## positive reviews summary
#     start = time.time()
#     tokens = pegasus_tokenizer(pos_reviews, truncation=True, padding='longest', return_tensors='pt')
#     end = time.time()
#     print(f"pos tokens = {round(end-start,3)}secs" )

#     start = time.time()
#     encoded_summary = pegasus_model.generate(**tokens, min_length=32, max_length=128, num_return_sequences=1,
#                                             decoder_start_token_id=pegasus_tokenizer.pad_token_id)
#     end = time.time()
#     print(f"encoded_summary = {round(end-start,3)}secs" )

#     start = time.time()
#     pos_encoded_summary = pegasus_tokenizer.decode(encoded_summary.squeeze(), skip_special_tokens=True)
#     end = time.time()
#     print(f"pos_encoded_summary = {round(end-start,3)}secs" )

#     ## negative reviews summary
#     start = time.time()
#     tokens = pegasus_tokenizer(neg_reviews, truncation=True, padding='longest', return_tensors='pt')
#     end = time.time()
#     print(f"neg tokens = {round(end-start,3)}secs" )

#     start = time.time()
#     encoded_summary = pegasus_model.generate(**tokens, min_length=32, max_length=128, num_return_sequences=1,
#                                             decoder_start_token_id=pegasus_tokenizer.pad_token_id)
#     end = time.time()
#     print(f"encoded_summary = {round(end-start,3)}secs" )

#     start = time.time()
#     neg_encoded_summary = pegasus_tokenizer.decode(encoded_summary.squeeze(), skip_special_tokens=True)
#     end = time.time()
#     print(f"neg_encoded_summary = {round(end-start,3)}secs" )
#     print("process_review ✅")
#     return pos_encoded_summary, neg_encoded_summary
