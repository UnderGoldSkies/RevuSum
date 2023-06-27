import pandas as pd

test_data_path = '/Users/zengsheng/code/TechLah/RevuSum/web_scraping/scraped_data_5.json' # test data json file path

# String to make the review text invalid
# Positive_Review: invalid reviews are with the following strings:
test_pos_invalid_content = 'there are no comments available for this review|everything'
# Negative_Review: invalid reviews are with the following strings:
test_neg_invalid_content = 'nothing|n/a|none'

# # Read JSON file into a DataFrame
## read the test data json file into a df
# with open(test_data_path, 'r') as f:
#     df = pd.read_json(f)


### 1. read the testd data json file into a df
###
""" function list:
1. get_hotel_reviews(df, hotel_name)
2. get_all_hotel_reviews(df)
"""

# a function to get all reviews from one hotel
def get_hotel_reviews(df, hotel_name):
    # Get the row of the DataFrame where the 'business_name' column is equal to the hotel_name
    hotel_df = df[df['business_name'] == hotel_name]

    # Get the review list from that hotel: reviews column first row
    reviews = hotel_df['reviews'].iloc[0]

    # Merge all rows of the 'reviews' column into one list
    reviews_list = [review for review in reviews]

    # Create a DataFrame from the list of dictionaries
    review_df = pd.DataFrame(reviews_list)

    #only keep 3 columns we needed, and rename the columns 'Negative_Review', 'Positive_Review', 'Review_Date',
    reviews_df_clean = review_df[['review_date', 'review_liked', 'review_disliked']]
    reviews_df_clean = reviews_df_clean.rename(columns={'review_date': 'Review_Date', 'review_liked': 'Positive_Review', 'review_disliked': 'Negative_Review'})

    # Add the 'Hotel_Name' column to the DataFrame
    reviews_df_clean['Hotel_Name'] = hotel_name

    # Move the 'Hotel_Name' column to the front of the DataFrame
    hotel_name_col = reviews_df_clean.pop('Hotel_Name')
    reviews_df_clean.insert(0, 'Hotel_Name', hotel_name_col)

    print(f"Created DataFrame with {len(reviews_df_clean)} rows.")
    # Return the DataFrame of reviews
    return reviews_df_clean


### Test the function ###
# # Get the reviews for the 'lyf Farrer Park Singapore' hotel
# review_df = get_hotel_reviews(df, 'lyf Farrer Park Singapore')
# print(review_df.head())

# define a function to loop through the hotel to get the reviews for a df from hotel json file
def get_all_hotel_reviews(df):
    # get all the business names(hotel name) to a list
    business_names = df['business_name'].tolist()

    result_df= pd.DataFrame()
    for hotel_name in business_names:

        #get the reviews for the hotel
        review_df = get_hotel_reviews(df, hotel_name)

        # concatenate the two dataframes along the rows
        result_df = pd.concat([result_df, review_df])


    return result_df

 ### test the function ###
# result_df = get_all_hotel_reviews(df)
# print(result_df.info())

### 2. clean the review text for the df
###
"""function list:
3. is_english(text)
4. clean_text(review_df, column_name, invalid_content_str)
5. clean_hotel_reviews(review_df, test_pos_invalid_content, test_neg_invalid_content)
"""

import numpy as np
from langdetect import detect


# define a function to check if a string is in English
def is_english(text):
    if not text: return True # an empty string is considered English
    try:
        lang = detect(text)
        return lang == 'en'
    except:
        return False

# define a function to do basic clean of the review text
def clean_text(review_df, column_name, invalid_content_str):
    # create the docstring for this function
    """
    # Input:
    # the review_df with 4 columns: 'Negative_Review', 'Positive_Review', 'Review_Date', 'Hotel_Name'
    # column_name: 'Negative_Review' or 'Positive_Review'
    #
    # Output:
    # a DataFrame with the same columns as review_df, but with invalid reviews removed
    # """


    english_reviews = review_df.copy()

    # convert to lowercase
    english_reviews[column_name] = english_reviews[column_name].str.lower()

    # apply strip() to remove leading and trailing whitespaces
    english_reviews[column_name] = english_reviews[column_name].apply(lambda x: x.strip())

    # filter out non-English reviews from the column
    english_reviews = review_df[review_df[column_name].apply(is_english)]

    # if the text contain invalid_content_str, replace the text with NAN
    english_reviews.loc[english_reviews[column_name].str.contains(invalid_content_str, case=False), column_name] = np.nan

    # if the text is empty, replace the text with NAN
    english_reviews.loc[english_reviews[column_name] == '', column_name] = np.nan
    return english_reviews

# define a function to clean the review text from one hotel dateframe
def clean_hotel_reviews(review_df, test_pos_invalid_content, test_neg_invalid_content):
    # clean the positive reviews
    cleaned_pos_df = clean_text(review_df, 'Positive_Review', test_pos_invalid_content)
    # clean the negative reviews
    cleaned_neg_df = clean_text(cleaned_pos_df, 'Negative_Review', test_neg_invalid_content)
    return cleaned_neg_df

### test the function ###
# cleaned_review_df = clean_hotel_reviews(review_df, test_pos_invalid_content, test_neg_invalid_content)
# print(cleaned_review_df.head())
