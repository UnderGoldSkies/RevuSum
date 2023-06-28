import pandas as pd
import yake



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
    kw_extractor = yake.KeywordExtractor(top=5, stopwords=None, windowsSize=1,n=1)
    mega_list = dataframe['Review'].tolist()
    combined_string = ''.join(mega_list)
    mega_words = kw_extractor.extract_keywords(combined_string)
    return mega_words
