import streamlit as st
from annotated_text import annotated_text, annotation
import time
from PIL import Image

st.title("RevuSUM")
st.markdown("""
RevuSum is a cutting-edge web app that simplifies hotel selection. Powered by AI, it generates concise summaries and insightful information from real visitor reviews. Say goodbye to manual review sifting - with RevuSum, access relevant summaries highlighting room quality, location, breakfast, cleanliness, and more. Make informed holiday choices with RevuSum's comprehensive insights.
""")

#image location parameter
image_location = 'img/' #local environment
#image_location = 'website/img/' #streamli cloud environment

img = Image.open(f'{image_location}village1.jpeg')
st.image(img)

#submit button
# Store the initial value of widgets in session state
if "visibility" not in st.session_state:
    st.session_state.visibility = "visible"
    st.session_state.disabled = False

# dropdown box
st.subheader("Select your hotel: ")

st.selectbox(
        " ",
        ("  ---Your Hotel Choice---  ", "Village Hotel Albert Court by Far East Hospitality", "Marian Hotel", "Chinatown One"),
        label_visibility = 'collapsed',
)


from dataclasses import dataclass
from time import sleep

import streamlit as st


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



#progress bar old
# progress_text = "Operation in progress. Please wait."
# my_bar = st.progress(0, text=progress_text)
# X = 9
# for percent_complete in range(100):
#     time.sleep(0.1)
#     my_bar.progress(percent_complete + 1, text=progress_text)

st.header("Hot topics: ")
annotated_text(
    ("location", "80%", "#afa"),
    "            ",
    ("staff", "70%", "#afa"),
    "            ",
    ("bed", "70%", "#afa"),
    "            ",
    ("room", "40%", "#faa"),
    "            ",
    ("breakfast", "10%", "#faa")
)

st.header("Review Summary: ")
with st.container():
    image_col, text_col = st.columns((0.2,2))
    with image_col:
        img = Image.open(f'{image_location}thumbsup.jpeg')
        st.image(img)


    with text_col:
        st.subheader("What people like about the hotel:")
        st.write("""The bed was so comfy, and the bathroom was good for the people who used a shataf
                 and for foreign people.the staff were also really nice. location was good,
                 metro walking distance, shops and restaurants close by. comfortable bed,
                 quite spacious for singapore, good air-conditioning - had tea and coffee making
                 facilities and a fridge. location was good close to station and short ride to gardens by the bay.
                 staff were great especially friendly johan, who seemed to be always there when we needed assistance,
                 very helpful. 1 minute walking from little india, plenty of indian restaurants, money exchange,
                 shopping area, mustafa
            """)
        #st.markdown("[Read more...](https://towardsdatascience.com/a-multi-page-interactive-dashboard-with-streamlit-and-plotly-c3182443871a)")

with st.container():
    image_col, text_col = st.columns((0.2,2))
    with image_col:
        img = Image.open(f'{image_location}thumbsdown.jpeg')
        st.image(img)

    with text_col:
        st.subheader("What people don't like about the hotel:")
        st.write("""
            Stayed for 7 days so a bit more variety in breakfast food especially the fruit would be nice but again for the price it was fine. it took some time to get hot water when taking shower. restaurant closed quite early and no option to get food late at night within hotel. wifi in room was poor but hotel did provide a spare wifi gadget so it worked out okay. almost good but an aircontrol at my room didn't work a little bit so i feeled a little hot.
            """)
