import pandas as pd
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from interface.testing import preprocess_of_test_data
from ml_logic.params import *
from ml_logic.sentiment_analysis import calculate_percentage, keywords_extract
from ml_logic.review_pegasus import main, load_tokenizer
import pickle

global df
global sentiment_model
global pegasus_model
global pegasus_tokenizer
global hotel_df
global preprocess_df

print("Fast API Started ✅")

# Load the test data from the file
df = pd.read_pickle(LOCAL_TEST_DATA_PATH)
print("Test data Loaded ✅")

# Load the model from the file
with open(SENTIMENT_MODEL_PATH, 'rb') as file:
    sentiment_model = pickle.load(file)
print("Sentiment Model Loaded ✅")

# Load the pegasus model from the file
with open(PEGASUS_MODEL_PATH, 'rb') as file:
    pegasus_model = pickle.load(file)
print("Pegasus Model Loaded ✅")

# # Load the pegasus tokenizer from the file
# with open(PEGASUS_TOKENIZER_PATH, 'rb') as file:
#     pegasus_tokenizer = pickle.load(file)
# print("Pegasus Tokenizer Loaded ✅")

pegasus_tokenizer = load_tokenizer()
print("Pegasus Tokenizer Loaded ✅")

preprocess_df = preprocess_of_test_data(df)


app = FastAPI()

# Allowing all middleware is optional, but good practice for dev purposes
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

#http://127.0.0.1:8000/predict?hotel_name=ibis%20Styles%20Singapore%20Albert
@app.get("/predict")
def predict(hotel_name: str):

    # # Load the test data from the file
    # df = pd.read_pickle(LOCAL_TEST_DATA_PATH)
    # print("Test data Loaded ✅")

    # # Load the model from the file
    # with open(SENTIMENT_MODEL_PATH, 'rb') as file:
    #     sentiment_model = pickle.load(file)
    # print("Sentiment Model Loaded ✅")

    # # Load the pegasus model from the file
    # with open(PEGASUS_MODEL_PATH, 'rb') as file:
    #     pegasus_model = pickle.load(file)
    # print("Pegasus Model Loaded ✅")

    # # # Load the pegasus tokenizer from the file
    # # with open(PEGASUS_TOKENIZER_PATH, 'rb') as file:
    # #     pegasus_tokenizer = pickle.load(file)
    # # print("Pegasus Tokenizer Loaded ✅")

    # pegasus_tokenizer = load_tokenizer()
    # print("Pegasus Tokenizer Loaded ✅")

    # hotel_df = df[df.Hotel_Name == hotel_name]
    # preprocess_df = preprocess_of_test_data(hotel_df)
    hotel_df = preprocess_df[preprocess_df.Hotel_Name == hotel_name]
    test_X = hotel_df['Review']
    test_y = hotel_df['Label']

    ypred = sentiment_model.predict(test_X)
    ypred=pd.Series(ypred, index=test_X.index)
    print("Prediction and index Completed ✅")

    results = pd.concat([test_X,ypred, test_y],axis=1)
    results.columns = ['Review', 'Pred', 'Label']
    print("Concate Completed ✅")

    keywordlist = keywords_extract(hotel_df)
    print("Extracted the keywords of all the reviews in a dict✅")

    return_dict = calculate_percentage(results,keywordlist)
    print("Dictionary updated with %Positive reviews for keywords ✅")

    positive_reviews, negative_reviews = main(df, hotel_name, pegasus_tokenizer, pegasus_model)
    print("Summary Completed ✅")

    return_dict.update({"Positive_Review":positive_reviews, "Negative_Review":negative_reviews})
    print("Dictionary updated with Summarized reviews ✅")

    return return_dict


@app.get("/")
def root():
    return {'greeting': 'Hello'}
