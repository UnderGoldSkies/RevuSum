import streamlit as st
from annotated_text import annotated_text, annotation
import time
from PIL import Image
from dataclasses import dataclass
from time import sleep
import requests


st.title("RevuSUM")
st.markdown("""
RevuSum is a cutting-edge web app that simplifies hotel selection. Powered by AI, it generates concise summaries and insightful information from real visitor reviews. Say goodbye to manual review sifting - with RevuSum, access relevant summaries highlighting room quality, location, breakfast, cleanliness, and more. Make informed holiday choices with RevuSum's comprehensive insights.
""")



# img = Image.open('website/img/village1.jpeg')    #streamlit cloud environment
img = Image.open('img/village1.jpeg')  #local environment
st.image(img)



#submit button
# Store the initial value of widgets in session state
if "visibility" not in st.session_state:
    st.session_state.visibility = "visible"
    st.session_state.disabled = False

# dropdown box
st.subheader("Select your hotel: ")

#defining a function to call api to get the prediction
def call_api():

    #user input: hotel name
    params = dict(hotel_name=hotel_selected)

    # get the json data from api:
    revusum_api_url = 'https://teamworkmakeswetdream-tddniu6ceq-ew.a.run.app/'
    response = requests.get(revusum_api_url, params=params)

    #return_dict = response.json()

hotel_selected = st.selectbox(
        " ",
        ("  ---Your Hotel Choice---  ", "Village Hotel Albert Court by Far East Hospitality", "Marian Hotel", "Chinatown One"),
        label_visibility = 'collapsed',
        on_change=reset_progress_bar
)

### dummy data
# return_dict = dict()
# return_dict.update({'location':0.82, 'service':0.72, 'breakfast':0.5, 'bed':0.3, 'cleanliness':0.91,
# 'Positive_Review': "The bed was so comfy, and the bathroom was good for the people who used a shataf and for foreign people.the staff were also really nice. location was good, metro walking distance, shops and restaurants close by. comfortable bed, quite spacious for singapore, good air-conditioning - had tea and coffee making facilities and a fridge. location was good close to station and short ride to gardens by the bay. staff were great especially friendly johan, who seemed to be always there when we needed assistance, very helpful. 1 minute walking from little india, plenty of indian restaurants, money exchange, shopping area, mustafa",
# 'Negative_Review': "Stayed for 7 days so a bit more variety in breakfast food especially the fruit would be nice but again for the price it was fine. it took some time to get hot water when taking shower. restaurant closed quite early and no option to get food late at night within hotel. wifi in room was poor but hotel did provide a spare wifi gadget so it worked out okay. almost good but an aircontrol at my room didn't work a little bit so i feeled a little hot."

### dummy data version- end



#color of keywords
Pos_color = "#afa"
Neg_color = "#faa"


# st.write(return_dict)
# st.write(type(return_dict))

# keywords_list=[]
# for key, value in return_dict.items():
#     if key == 'Positive_Review':
#         positive_sum = value
#     elif key == 'Negative_Review':
#         negative_sum = str(value)
#     else:
#         if float(value) > 0.5:
#             keywords_list.append((key, value, Pos_color))
#         else:
#             keywords_list.append((key, value, Neg_color))




@dataclass
class Program:
    progress: int = 0
    def predict(self):
        for i in [10, 30, 50, 70, 100]:
            self.progress = i
            sleep(1)
            my_bar.progress(p.progress, text=f"Progress: {p.progress}%")

    def increment(self):
        self.progress += 1
        sleep(0.1)


my_bar = st.progress(0, text="Operation in progress. Please wait...")

p = Program()

while p.progress < 100:
    p.predict()
    # my_bar.progress(p.progress, text=f"Progress: {p.progress}%")




st.header("Hot topics: ")
annotated_text(
    [
    annotation("staff", "80%", font_size='20px', background="#afa"),
    annotation("   ", styles="padding-right: 50px; background-color: #FFFFFF;"),
    annotation("room", "70%", font_size='20px', background="#afa"),
    annotation("   ", styles="padding-right: 50px; background-color: #FFFFFF;"),
    annotation("location", "80%", font_size='20px', background="#afa"),
    annotation("   ", styles="padding-right: 50px; background-color: #FFFFFF;"),
    annotation("breakfast", "10%", font_size='20px', background="#faa")
    ]
)
#annotation("staff", "80%", color="#afa", font_size='20px', font_family="Comic Sans MS", border="2px dashed red"),


# # all the varibles:
positive_sum = """The bed was so comfy, and the bathroom was good for the people who used a shataf
                 and for foreign people.the staff were also really nice. location was good,
                 metro walking distance, shops and restaurants close by. comfortable bed,
                 quite spacious for singapore, good air-conditioning - had tea and coffee making
                 facilities and a fridge. location was good close to station and short ride to gardens by the bay.
                 staff were great especially friendly johan, who seemed to be always there when we needed assistance,
                 very helpful. 1 minute walking from little india, plenty of indian restaurants, money exchange,
                 shopping area, mustafa
            """
negative_sum = """The room was very small and the bathroom was not clean. the room was very small and the bathroom was not clean."""

st.header("Review Summary: ")
with st.container():
    image_col, text_col = st.columns((0.2,2))
    with image_col:
        # img = Image.open('website/img/thumbsup.jpeg')    #streamlit cloud environment
        img = Image.open('img/thumbsup.jpeg')  #local environment
        st.image(img)


    with text_col:
        st.subheader("What people like about the hotel:")
        st.write(positive_sum)
        #st.markdown("[Read more...](https://towardsdatascience.com/a-multi-page-interactive-dashboard-with-streamlit-and-plotly-c3182443871a)")

with st.container():
    image_col, text_col = st.columns((0.2,2))
    with image_col:
        # img = Image.open('website/img/thumbsdown.jpeg')    #streamlit cloud environment
        img = Image.open('img/thumbsdown.jpeg')  #local environment
        st.image(img)

    with text_col:
        st.subheader("What people don't like about the hotel:")
        st.write(negative_sum)
