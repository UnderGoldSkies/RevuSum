import streamlit as st
from annotated_text import annotated_text, annotation
import time
from PIL import Image
from dataclasses import dataclass
from time import sleep
import requests
import os
import pandas as pd

keywords_list=[]
positive_sum =''
negative_sum =''
default_hotel_name = "  ---Your Hotel Choice---  "
#color of keywords
Pos_color = "#afa"
Neg_color = "#faa"

#dummy data for testing
return_dict = dict()
return_dict.update({'location':0.82, 'service':0.755, 'breakfast':0.567, 'bed':0.321, 'cleanliness':0.91,
'Positive_Review': "The bed was so comfy, and the bathroom was good for the people who used a shataf and for foreign people.the staff were also really nice. location was good, metro walking distance, shops and restaurants close by. comfortable bed, quite spacious for singapore, good air-conditioning - had tea and coffee making facilities and a fridge. location was good close to station and short ride to gardens by the bay. staff were great especially friendly johan, who seemed to be always there when we needed assistance, very helpful. 1 minute walking from little india, plenty of indian restaurants, money exchange, shopping area, mustafa",
'Negative_Review': "Stayed for 7 days so a bit more variety in breakfast food especially the fruit would be nice but again for the price it was fine. it took some time to get hot water when taking shower. restaurant closed quite early and no option to get food late at night within hotel. wifi in room was poor but hotel did provide a spare wifi gadget so it worked out okay. almost good but an aircontrol at my room didn't work a little bit so i feeled a little hot."
})


def process_result(hotel_selected):
    # #call api
    # url = 'https://teamworkmakeswetdream-tddniu6ceq-ew.a.run.app/predict'
    # params = dict(hotel_name=hotel_selected)
    # response = requests.get(url, params=params)
    # return_dict = response.json()

    for key, value in return_dict.items():
        if key == 'Positive_Review':
            positive_sum = value
        elif key == 'Negative_Review':
            negative_sum = value
        else:
            value_str = f'{round(value * 100)} %'
            key = key.capitalize()
            if value > 0.5:
                keywords_list.append(annotation(key, value_str, font_size='20px', background=Pos_color))
            else:
                keywords_list.append(annotation(key, value_str, font_size='20px', background=Neg_color))
            keywords_list.append(annotation('   ', styles='padding-right: 50px; background-color: #FFFFFF;'))
    return positive_sum, negative_sum

def load_hotel_name():
    url = os.getcwd() +  '/website/cleaned_test_data_5.pkl' #streamlit cloud environment
    #url = '/cleaned_test_data_5.pkl' #local environment
    raw_df = pd.read_pickle(url)
    hotel_list = [default_hotel_name]
    for hotel_name in raw_df['Hotel_Name'].unique():
        hotel_list.append(hotel_name)
    return hotel_list

#get the hotel name list
hotel_list = load_hotel_name()


st.title("RevuSUM")
st.markdown("""
RevuSum is a cutting-edge web app that simplifies hotel selection. Powered by AI, it generates concise summaries and insightful information from real visitor reviews. Say goodbye to manual review sifting - with RevuSum, access relevant summaries highlighting room quality, location, breakfast, cleanliness, and more. Make informed holiday choices with RevuSum's comprehensive insights.
""")

img = Image.open('website/img/village1.jpeg')    #streamlit cloud environment
# img = Image.open('img/village1.jpeg')  #local environment
st.image(img)


# dropdown box
st.subheader("Select your hotel: ")
hotel_selected = st.selectbox(
        " ",
        (hotel_list),
        label_visibility = 'collapsed',
)
## if a hotel is selected, show the result
if hotel_selected != default_hotel_name:
    # initiate the Progress bar
    my_bar = st.progress(0, text=f"Checking for {hotel_selected}. Please wait...")

    # start the progress bar
    for i in [1, 3, 5, 7]:
        progress = i
        time.sleep(0.5)
        my_bar.progress(progress, text=f"Checking for {hotel_selected}. Please wait... {progress}%")

    # call API
    positive_sum, negative_sum = process_result(hotel_selected)


    for i in [95,97,100]:
        progress = i
        time.sleep(0.5)
        my_bar.progress(progress, text=f"Progress: {progress}%")

    #To show the hotel review data
    st.header("Hot topics: ")
    annotated_text(keywords_list)


    st.header("Review Summary: ")
    with st.container():
        image_col, text_col = st.columns((0.2,2))
        with image_col:
            img = Image.open('website/img/thumbsup.jpeg')    #streamlit cloud environment
            # img = Image.open('img/thumbsup.jpeg')  #local environment
            st.image(img)


        with text_col:
            st.subheader("What people like about the hotel:")
            st.write(positive_sum)
            #st.markdown("[Read more...](https://towardsdatascience.com/a-multi-page-interactive-dashboard-with-streamlit-and-plotly-c3182443871a)")

    with st.container():
        image_col, text_col = st.columns((0.2,2))
        with image_col:
            img = Image.open('website/img/thumbsdown.jpeg')    #streamlit cloud environment
            # img = Image.open('img/thumbsdown.jpeg')  #local environment
            st.image(img)

        with text_col:
            st.subheader("What people don't like about the hotel:")
            st.write(negative_sum)

##


# @dataclass
# class Program:
#     progress: int = 0
#     def predict(self):
#         for i in [10, 30, 50, 70, 100]:
#             self.progress = i
#             sleep(1)
#             my_bar.progress(p.progress, text=f"Progress: {p.progress}%")

#     def increment(self):
#         self.progress += 1
#         sleep(0.1)


# my_bar = st.progress(0, text="Operation in progress. Please wait...")

# p = Program()

# while p.progress < 100:
#     p.predict()
#     # my_bar.progress(p.progress, text=f"Progress: {p.progress}%")
