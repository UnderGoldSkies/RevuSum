import pandas as pd
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from interface.main import preprocess_of_test_data
from ml_logic.params import *
from ml_logic.sentiment_analysis import calculate_percentage, keywords_extract
from ml_logic.review_pegasus import main
import pickle
# import torch
from timeit import default_timer as timer


global df
global sentiment_model
global hotel_df
global preprocess_df
# global cpu_bart_model
# global bart_tokenizer

print("Fast API Started ✅")

# Load the test data from the file
df = pd.read_pickle(LOCAL_TEST_DATA_PATH)
print("Test data Loaded ✅")

# Load the model from the file
# Temporary comment out by Haris
# with open(SENTIMENT_MODEL_PATH, 'rb') as file:
#     sentiment_model = pickle.load(file)
# print("Sentiment Model Loaded ✅")



preprocess_df = preprocess_of_test_data(df)

#set the google auth env variable
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = GOOGLE_CREDENTIAL_PATH
print('Google credential assigned ✅')

app = FastAPI()

# Allowing all middleware is optional, but good practice for dev purposes
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

@app.get("/predict")
def predict(hotel_name: str):

    hotel_df = preprocess_df[preprocess_df.Hotel_Name == hotel_name]
    test_X = hotel_df['Review']
    test_y = hotel_df['Label']

    start = timer()
    ypred = sentiment_model.predict(test_X)
    ypred=pd.Series(ypred, index=test_X.index)
    end = timer()
    print(f"Prediction and index Completed ✅ {round(end-start,3)}secs")


    start = timer()
    results = pd.concat([test_X,ypred, test_y],axis=1)
    results.columns = ['Review', 'Pred', 'Label']
    end = timer()
    print(f"Concate Completed ✅ {round(end-start,3)}secs")


    start = timer()
    keywordlist = keywords_extract(hotel_df)
    end = timer()
    print(f"Extracted the keywords of all the reviews in a dict✅ {round(end-start,3)}secs")


    start = timer()
    return_dict = calculate_percentage(results,keywordlist)
    end = timer()
    print(f"Dictionary updated with %Positive reviews for keywords ✅ {round(end-start,3)}secs ")

    start = timer()
    (positive_reviews, negative_reviews) = main(df, hotel_name)
    end = timer()
    print(f"Summary Completed ✅ {round(end-start,3)}secs")


    start = timer()
    return_dict.update({"Positive_Review":positive_reviews, "Negative_Review":negative_reviews})
    end = timer()
    print(f"Dictionary updated with Summarized reviews ✅ {round(end-start,3)}secs")

    return return_dict

@app.get('/temp_summary')
def temporary_summary(hotel_name: str):
    return_dict = dict()
    start = timer()
    (positive_reviews, negative_reviews) = main(df, hotel_name)
    end = timer()
    print(f"Summary Completed ✅ {round(end-start,3)}secs")

    start = timer()
    return_dict.update({"Positive_Review":positive_reviews, "Negative_Review":negative_reviews})
    end = timer()
    print(f"Dictionary updated with Summarized reviews ✅ {round(end-start,3)}secs")
    return return_dict

@app.get("/")
def root():
    return {'greeting': 'Hello'}

# (Unused) Load the pegasus model from the file
# with open(CPU_BART_MODEL_PATH, 'rb') as file:
#     cpu_bart_model = pickle.load(file)
# print("cpu_bart_model Loaded ✅")

# bart_tokenizer = load_bart_tokenizer()
# print("bart_tokenizer Loaded ✅")
