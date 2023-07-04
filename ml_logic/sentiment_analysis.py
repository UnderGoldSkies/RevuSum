import pandas as pd
import yake
from nltk.corpus import stopwords



def calculate_percentage(results:pd.DataFrame,keywordlist):
    #call function to generate keywords

    return_dict=dict()
    for number in range(0,5):
        keyword = keywordlist[number][0]
        keyword_bool = results['Review'].str.contains(keyword)
        results_bool = results[keyword_bool]
        pos_reviews_percentage = round(results_bool.Pred.sum()/len(results_bool),2)
        return_dict.update({keyword: pos_reviews_percentage})

    return return_dict


def keywords_extract(dataframe):
    # kw_extractor = yake.KeywordExtractor(top=5, stopwords=None, windowsSize=1,n=1)
    # mega_list = dataframe['Review'].tolist()
    # combined_string = ''.join(mega_list)
    # mega_words = kw_extractor.extract_keywords(combined_string)
    stopwords_list = stopwords.words('english')
    # Append new words to the stopwords list
    custom_words = ['good', 'bad', 'nice', 'small', 'little']
    stopwords_list.extend(custom_words)
    kw_extractor = yake.KeywordExtractor(top=5, stopwords=stopwords_list, windowsSize=1,n=1)
    mega_list = dataframe['Review'].tolist()
    combined_string = ''.join(mega_list)
    mega_words = kw_extractor.extract_keywords(combined_string)
    return mega_words


def calculate_percentage_keyword(results,keyword):
    return_dict=dict()
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
        # handle the case when 10 or more values are True
        results_bool = results[keyword_bool]
        review_count_of_kw = len(results_bool)
        pos_reviews_percentage = round(results_bool.Pred.sum()/review_count_of_kw,2)
        return_dict.update({keyword: pos_reviews_percentage})
        print(f"✅ Generating based on keywords")
        return return_dict


def show_reviews(results,keyword):
    keyword_bool = results['Review'].str.contains(keyword)
    if keyword_bool.sum() > 10:
        # handle the case when there are more than 10 reviews to display
        print(f"❌ Limit exceeded, Maximum display of 10 reviews")
        return {"message": "❌ Limit exceeded, Maximum display of 10 reviews"}

    else:
        # handle the case when there are less than 10 reviews to display
        results_bool = results[keyword_bool]
        review_list = results_bool['Review'].tolist()
        review_text = '\n '.join(review_list)
        print("✅ List of reviews with keywords")
        return {'reviews': review_text}
