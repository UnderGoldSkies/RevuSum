from nltk.corpus import stopwords
import yake


def keywordextracter(dataframe):
    stopwords_list = stopwords.words('english')
    # Append new words to the stopwords list
    custom_words = ['good', 'bad', 'nice', 'small', 'little']
    stopwords_list.extend(custom_words)
    kw_extractor = yake.KeywordExtractor(top=5, stopwords=stopwords_list, windowsSize=1,n=1)
    mega_list = dataframe['Review'].tolist()
    combined_string = ''.join(mega_list)
    mega_words = kw_extractor.extract_keywords(combined_string)
    return mega_words
