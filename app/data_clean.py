import pandas as pd


# def a function to clean the df reviews data
def clean_reviews(df, negative_review, positive_review, Review_Date, Hotel_Name):
    """
    Input:
    # df: a dataframe with hotel reviews
    # negative_review: a string of the column name of the negative reviews
    # positive_review: a string of the column name of the positive reviews
    # Review_Date: a string of the column name of the review date
    # Hotel_Name: a string of the column name of the hotel name
    Output:
    # return a dataframe with 4 columns: 'Negative_Review', 'Positive_Review', 'Review_Date', 'Hotel_Name'

    Todo:Clean the reviews from the dataset
    #removing invalid ones, e.g. empty reviews, everything is good/bad and reviews with less than 10 characters
    """

    # process the Negative_Review column
    # strip() to remove leading and trailing whitespaces for one column of df
    df['Negative_clean'] = df[negative_review].apply(lambda x: x.strip())

    # if the text has less than 10 characters, replace the text with ' ' for the above column
    df.loc[df['Negative_clean'].str.len() < 10, 'Negative_clean'] = ' '

    # if the text has 'nothing' or 'everything' or 'anything' str in it regardless lower case, replace the text with ' ' for the above column
    df.loc[df['Negative_clean'].str.contains('nothing|everything|anything|No Negative', case=False), 'Negative_clean'] = ' '


    # do the same process for Positive_Review column
    df['Positive_clean'] = df[positive_review].apply(lambda x: x.strip())

    # if the text has less than 10 characters, replace the text with ' ' for the above column
    df.loc[df['Positive_clean'].str.len() < 10, 'Positive_clean'] = ' '

    # if the text has 'nothing' or 'everything' or 'No Positive' str in it regardless lower case, replace the text with 'nothing' for the above column
    df.loc[df['Positive_clean'].str.contains('nothing|everything|No Positive', case=False), 'Positive_clean'] = ' '

    # change column names to another set of names for the df
    df.rename(columns={negative_review: 'Negative_Review', positive_review: 'Positive_Review', Review_Date: 'Review_Date', Hotel_Name: 'Hotel_Name'}, inplace=True)

    # return the df with 4 columns: 'Negative_Review', 'Positive_Review', 'Review_Date', 'Hotel_Name'
    return df[['Negative_Review', 'Positive_Review', 'Review_Date', 'Hotel_Name']]

#test the function
#import data from a csv file and store in a dataframe
df = pd.read_csv('data/Hotel_Reviews.csv')

df_new = clean_reviews(df, 'Negative_Review', 'Positive_Review', 'Review_Date', 'Hotel_Name')
print(df_new.shape, df_new.columns)

#Can save the df_new to a csv file
# df_new.to_csv('data/Hotel_Reviews_clean.csv', index=False)
