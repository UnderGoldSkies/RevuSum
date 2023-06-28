


def keywordextracter(dataframe):
    kw_extractor = yake.KeywordExtractor(top=5, stopwords=None, windowsSize=1,n=1)
    mega_list = dataframe['Review'].tolist()
    combined_string = ''.join(mega_list)
    mega_words = kw_extractor.extract_keywords(combined_string)
    return mega_words
