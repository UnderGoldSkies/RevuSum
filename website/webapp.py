import streamlit as st
from annotated_text import annotated_text, annotation
import time
from PIL import Image
from dataclasses import dataclass
from time import sleep
import requests
import os
import pandas as pd
import base64

keywords_list=[]
positive_sum =''
negative_sum =''
default_hotel_name = " "
#color of keywords
Pos_color = "#afa"
Neg_color = "#faa"
#switch file path between
file_path = 'website/' #streamlit cloud environment
# file_path = '' #local environment

# #dummy data for testing, 111
# return_dict = dict()
# return_dict.update({'location':0.82, 'service':0.755, 'breakfast':0.567, 'bed':0.321, 'cleanliness':0.91,
# 'Positive_Review': "The bed was so comfy, and the bathroom was good for the people who used a shataf and for foreign people.the staff were also really nice. location was good, metro walking distance, shops and restaurants close by. comfortable bed, quite spacious for singapore, good air-conditioning - had tea and coffee making facilities and a fridge. location was good close to station and short ride to gardens by the bay. staff were great especially friendly johan, who seemed to be always there when we needed assistance, very helpful. 1 minute walking from little india, plenty of indian restaurants, money exchange, shopping area, mustafa",
# 'Negative_Review': "Stayed for 7 days so a bit more variety in breakfast food especially the fruit would be nice but again for the price it was fine. it took some time to get hot water when taking shower. restaurant closed quite early and no option to get food late at night within hotel. wifi in room was poor but hotel did provide a spare wifi gadget so it worked out okay. almost good but an aircontrol at my room didn't work a little bit so i feeled a little hot."
# })
# #dummy data for testing, 111

def process_result(hotel_selected):
    #call api, 111
    url = 'https://revusumbison-jso3izqmjq-ew.a.run.app/'
    params = dict(hotel_name=hotel_selected)
    response = requests.get(url, params=params)
    return_dict = response.json()
    #call api, 111

    for key, value in return_dict.items():
        if key == 'Positive_Review':
            positive_sum = value
        elif key == 'Negative_Review':
            negative_sum = value
        else:
            value_str = f'{round(value * 100)} %✔️'
            key = key.capitalize()
            if value > 0.5:
                keywords_list.append(annotation(key, value_str, font_size='18px', background=Pos_color))
            else:
                keywords_list.append(annotation(key, value_str, font_size='18px', background=Neg_color))
            keywords_list.append(annotation('   ', styles='padding-right: 40px; background-color: rgba(255,255,255,0);'))
    return positive_sum, negative_sum

def load_hotel_name():
    # url = os.getcwd() +  '/website/cleaned_test_data_5.pkl' #streamlit cloud environment
    url = f'{file_path}cleaned_test_data_5.pkl' #  local environment
    raw_df = pd.read_pickle(url)
    hotel_list = [default_hotel_name]
    for hotel_name in raw_df['Hotel_Name'].unique():
        hotel_list.append(hotel_name)
    return hotel_list

#get the hotel name list
hotel_list = load_hotel_name()

# define a function to show hotel top html content
def top_html(hotel_selected):
    address = '277 Orchard Road, Orchard, 238858 Singapore, Singapore'
    total_reviews = '2,294'
    score_text = 'Very Good'
    score_point = '8.4'
    #create a image url list
    image_urls = ['https://cf2.bstatic.com/xdata/images/hotel/max500/327961860.jpg?k=40c2e566b3c5f462f8a18df6cd0476ca1334801767097d41b353b96259327562&amp;o=&amp;hp=1',
                      'https://cf2.bstatic.com/xdata/images/hotel/max500/327961868.jpg?k=284648f1385a9ae8e8c74ebf0b7d20583d4f38289121c17f407f23d8dbbea33b&amp;o=&amp;hp=1',
                      'https://cf2.bstatic.com/xdata/images/hotel/max1024x768/326893205.jpg?k=977021538d51e8e7d1ee65fd16d26db58547c263f681d78ad6f3f8bb41837865&amp;o=&amp;hp=1']

    top_html = f"""<div >
                        <h2  style="display: flex; justify-content: space-between; align-items: center; font-family: 'Avenir Next'; font-size: 24px; padding:0px; margin:0%">{hotel_selected}</h2>
                    </div>
                <div style="display: flex; justify-content: space-between; align-items: center; font-size: 15px; ">
                <div style="flex: 1; padding-right: 10px;">{address}</div>
                <div style="display: flex; justify-content: space-between; align-items: center;  padding: 5px;">
                    <div style="display: flex; flex-direction: column; padding: 5px;">
                    <div style="font-size: 16px; font-weight: bold;">{score_text}</div>
                    <div style="font-size: 12px;">{total_reviews} reviews</div>
                    </div>
                    <div style="font-size: 16px; font-weight: bold;background-color: blue; color: white; padding: 5px;">{score_point}</div>
                </div>
                </div>
                <div style="display: flex; justify-content: space-between;">
                <div style="display: flex; flex-direction: column; flex: 1; margin-right: 10px;">
                    <div><img src="{image_urls[0]}" style="width: 100%; height: auto; margin-top: auto; margin-bottom: 10px;"></div>
                    <div></div><img src="{image_urls[1]}" style="width: 100%; height: auto; margin-top: auto;">
                </div>
                <div style="display: flex; align-items: flex-end; flex: 2;">
                    <img src="{image_urls[2]}" style="width: 100%; height: auto;">
                </div>
                </div>"""
    return top_html

#convert two thumb image to base64
with open(f"{file_path}img/thumbsup.png", "rb") as image_file:
    encoded_string_up = base64.b64encode(image_file.read()).decode('utf-8')
with open(f"{file_path}img/thumbsdown.png", "rb") as image_file:
    encoded_string_down = base64.b64encode(image_file.read()).decode('utf-8')


def summary_html(positive_sum,negative_sum):
    html_code = f'''
                <div style="display: flex; justify-content: space-between; align-items: flex-start;">
                <div style="flex: 0.2; text-align: center;">
                    <img src="data:image/jpeg;base64,{ encoded_string_up }" alt="Image" width="56" height="56" style="display: block; margin: 0 auto;">
                </div>
                <div style="flex: 2;">
                    <div style="flex: 1; font-size: 20px; font-weight: bold; padding-right: 10px;">What people like about the hotel:</div>
                    <p>{ positive_sum }</p>
                </div>
                </div>
                <div style="display: flex; justify-content: space-between; align-items: flex-start;">
                <div style="flex: 0.2; text-align: center;">
                    <img src="data:image/jpeg;base64,{ encoded_string_down }" alt="Image" width="56" height="56" style="display: block; margin: 0 auto;">
                </div>
                <div style="flex: 2;">
                    <div style="flex: 1; font-size: 20px; font-weight: bold; padding-right: 10px;">What people don't like about the hotel:</div>
                    <p>{ negative_sum }</p>
                </div>
                </div>
    '''

    return html_code

# st.title("RevuSUM")
# st.markdown("""
# RevuSum is a cutting-edge web app that simplifies hotel selection. Powered by AI, it generates concise summaries and insightful information from real visitor reviews. Say goodbye to manual review sifting - with RevuSum, access relevant summaries highlighting room quality, location, breakfast, cleanliness, and more. Make informed holiday choices with RevuSum's comprehensive insights.
# """)

def get_base64(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()


def set_background(png_file):
    bin_str = get_base64(png_file)
    page_bg_img = '''
    <style>
    .stApp {
    background-image: url("data:image/png;base64,%s");
    background-size: cover;
    }
    </style>
    ''' % bin_str
    st.markdown(page_bg_img, unsafe_allow_html=True)

#set the background
set_background(f"{file_path}img/hotel_on_lake.jpeg")


# adjust spacing
st.write(' ')
st.write(' ')
st.write(' ')
st.write(' ')
st.write(' ')
st.write(' ')
st.write(' ')
st.write(' ')
st.write(' ')
st.write(' ')
st.write(' ')


# with st.container():
#logo
# img = Image.open('website/img/logo3.jpeg')  #streamlit cloud environment
img = Image.open(f'{file_path}img/logo3.jpeg')  #local environment
st.image(img, width=240)

# dropdown box Title
st.subheader(" :violet[Pick Your Hotel]")

# select box
hotel_selected = st.selectbox(
        " ",
        (hotel_list),
        label_visibility = 'collapsed',
)

## if a hotel is selected, show the result
if hotel_selected != default_hotel_name:
    # initiate the Progress bar
    # st.markdown("<span style='font-size: 30px; color: blue; font-weight: bold;'> Progress: </span>", unsafe_allow_html=True)
    my_bar = st.progress(0)

    # add a big container
    with st.container():


        # generate the top html content
        top_html = top_html(hotel_selected)

        # start the progress bar
        for i in [1, 3, 5, 7]:
            progress = i
            time.sleep(0.1)
            my_bar.progress(progress)


        # call API
        positive_sum, negative_sum = process_result(hotel_selected)


        for i in [95,97,100]:
            progress = i
            time.sleep(0.1)
            my_bar.progress(progress)

        # show the top html content
        st.markdown(top_html, unsafe_allow_html=True)

        #To show the hotel review data
        st.subheader("Hot topics: ")
        annotated_text(keywords_list)


        st.subheader("Review Summary: ")

        # generate the summary html content
        summary = summary_html(positive_sum,negative_sum)
        # show the top html content
        st.markdown(summary, unsafe_allow_html=True)

        st.markdown(
                        """
                    <style>
                        div[data-testid="stVerticalBlock"] div[style*="flex-direction: column;"] div[data-testid="stVerticalBlock"] {
                            background-color: rgba(255,255,255,0.6);
                            padding: 15px;
                            border-radius: 8px;
                            width: 730px;
                        }
                    </style>
                    """,
                        unsafe_allow_html=True,
                    )
