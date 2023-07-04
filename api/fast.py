import pandas as pd
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from interface.main import preprocess_of_test_data, preprocess_keyword
from ml_logic.params import *
from ml_logic.sentiment_analysis import calculate_percentage, keywords_extract, calculate_percentage_keyword, show_reviews
from ml_logic.review_pegasus import main, process_keyword
import pickle
from timeit import default_timer as timer


global df
global sentiment_model
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



preprocess_df = preprocess_of_test_data(df)

#set the google auth env variable
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = GOOGLE_CREDENTIAL_PATH
print('Google credential assigned ✅')
print(os.environ["GOOGLE_APPLICATION_CREDENTIALS"])

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


@app.get("/predict_hotel_keyword")
def predict_hotel_keyword(hotel_name: str, keyword: str):
    print('Predict Hotel Keyword')

    keyword = preprocess_keyword(keyword)
    print(f"keyword preprocessed✅")

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

    keyword_bool = results['Review'].str.contains(keyword)

    if keyword_bool.sum() == 0:
        # handle the case when no value is True
        print(f"❌ Topics not found in reviews")
        return {"message": "❌ Topics not found in reviews"}

    elif keyword_bool.sum() >= 1 and keyword_bool.sum() < 10:
        results_bool = results[keyword_bool]
        # handle the case when at least 1 value is True but less than 10 values are True
        print(f"❌ Insufficient data to generate informative sentiments")
        return {
        "message": "❌ Insufficient data to generate informative sentiments/ reviews,"
                   "use Display Reviews to read each review."
                }

    else:
        results_bool = results[keyword_bool]
        return_dict = calculate_percentage_keyword(results,keyword)
        print(results_bool.shape, results.shape)
        print(results_bool.columns)
        print(results_bool)

        start = timer()
        (positive_reviews, negative_reviews) = process_keyword(df, hotel_name, keyword)
        end = timer()
        print(f"Summary Completed ✅ {round(end-start,3)}secs")

        start = timer()
        return_dict.update({"Positive_Review":positive_reviews, "Negative_Review":negative_reviews})
        end = timer()

        print(f"Dictionary updated with Summarized reviews ✅ {round(end-start,3)}secs")

        return return_dict


@app.get("/read_keyword_review")
def read_keyword_review(hotel_name: str, keyword: str):

    keyword = preprocess_keyword(keyword)
    print(f"keyword preprocessed✅")

    hotel_df = preprocess_df[preprocess_df.Hotel_Name == hotel_name]
    test_X = hotel_df['Review']
    test_y = hotel_df['Label']

    start = timer()
    ypred = sentiment_model.predict(test_X)
    ypred=pd.Series(ypred, index=test_X.index)
    end = timer()
    print(f"Prediction and index Completed ✅ {round(end-start,3)}secs")


    start = timer()
    results = pd.concat([test_X, ypred, test_y],axis=1)
    results.columns = ['Review', 'Pred', 'Label']
    end = timer()
    print(f"Concate Completed ✅ {round(end-start,3)}secs")


    return show_reviews(results,keyword)


@app.get("/")
def root():
    return {'greeting': 'Hello'}
