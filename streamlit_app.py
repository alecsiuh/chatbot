import streamlit as st
from datetime import datetime
import os
from Chatbot.OpenAi.openai_client import OpenAIClient
import pandas as pd
import io 
import gspread
from google.oauth2.service_account import Credentials
from PIL import Image


# Get the API key from the environment
api_key = os.getenv("OPENAI_API_KEY")

# Initialize your chatbot client with the API key from the environment
# Initialize chatbot if not already initialized
if "chatbot" not in st.session_state:
    st.session_state.chatbot = OpenAIClient(api_key=api_key)


# Authorize Google Sheets API
def init_google_sheets_client(json_credentials):
    scope = ['https://www.googleapis.com/auth/spreadsheets',
             'https://www.googleapis.com/auth/drive']
    credentials = Credentials.from_service_account_info(json_credentials, scopes=scope)
    return gspread.authorize(credentials)


# Load service account credentials from Streamlit secrets
json_credentials = st.secrets["gcp_service_account"]

# Open the Google Sheet
spreadsheet_name = 'https://docs.google.com/spreadsheets/d/18_AAt6mSaEaCPraqX8Tm_nDrTbUYAG-zva8XrxXS9rQ/edit?usp=sharing'
worksheet_name = 'Sheet1'

def display_png_image(png_data):
    image = Image.open(io.BytesIO(png_data))
    st.image(image, caption='Displayed PNG Image')

### STYLING ### 
st.markdown(
    """
    <style>
    .st-emotion-cache-1xw8zd0.e10yg2by1 {
        position: relative;
        margin-top: 120%;
        bottom: 0;
        width: 100%;
    }
    .st-emotion-cache-16txtl3.eczjsme4 {
        padding-top: 0;
        padding-bottom: 0;
        height: 100%;
    }
    .st-emotion-cache-k7vsyb.e1nzilvr2 {
        margin-top: 1em;
    }
    .st-emotion-cache-ch5dnh.ef3psqc5, .st-emotion-cache-6q9sum.ef3psqc4 {
        visibility: hidden;
    }
    .st-emotion-cache-r421ms.e10yg2by1 {
        border: none; 
    } 
    .st-at.st-au.st-av.st-aw.st-ae.st-ag.st-ah.st-af.st-c2.st-bo.st-c3.st-c4.st-c5.st-c6.st-am.st-an.st-ao.st-ap.st-c7.st-ar.st-as.st-bb.st-ax.st-ay.st-az.st-b0.st-b1 {
        width: 70%; 
        justify-content: space-between;
    } 
    .st-emotion-cache-bho8sy.eeusbqq1 {
        background-color: #7547FF;
    }
    .st-emotion-cache-1ghhuty.eeusbqq1 { 
        background-color: #E5B7E5;
    } 
    .st-emotion-cache-6qob1r.eczjsme3 { 
        border-top-right-radius: 1rem; 
        border-bottom-right-radius: 1rem;
        color: white;
        background-color: #7547FF;
        width: 20rem;
    }   
    .st-emotion-cache-1sva07 {
        display: none;
    }
    .st-emotion-cache-k7vsyb.e1nzilvr2 {
        color: #FFFFFF;
    } 
    .st-emotion-cache-16txtl3 h1, .st-emotion-cache-16txtl3 h2, .st-emotion-cache-l9bjmx p {
        color: #FFFFFF;
    }
    .st-emotion-cache-163zt37.ef3psqc7 {
        color: #7547FF;
    }
    .stAlert {
        background-color: aliceblue;
        border-radius: 0.5rem;
    }  
    .st-emotion-cache-1h9usn1.eqpbllx4 {
        border: none; 
    }
    """,
    unsafe_allow_html=True,
)

st.sidebar.title("The Lab - FAN app")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Hello there! Ask me anything about the data that interests you. I'm here to help you!"}]

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("What is up?"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Display user input in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)  # Display the user's input 
        response = st.session_state.chatbot.get_gpt3_response(prompt)

    # if the assistant response is a dataframe, display it as an interactive table
    if isinstance(response, pd.DataFrame):
        st.dataframe(response)
        st.session_state.messages.append({"role": "assistant", "content": f"```{response.head(5)}```"}) 
    # if the assistant response holds image data, Display the image
    elif isinstance(response, bytes):
        display_png_image(response)
        st.session_state.messages.append({"role": "assistant", "content": "Displayed PNG Image"})
    else:
        # Display assistant response in chat message container and add to chat history
        with st.chat_message("assistant"):
            st.markdown(response)  # Display the chatbot response
        st.session_state.messages.append({"role": "assistant", "content": response})


### SUGGESTIVE PROMPTS ###
# Initialize the suggestion chosen state
if 'suggestion_chosen' not in st.session_state:
    st.session_state.suggestion_chosen = False 

suggestions = ["What topics are covered?", "Find datasets about education.", "Show me a dataset that relates to the unemployment rate in Antwerpen.", 
               "How can I visualize the evolution of data over the years?"]

if not st.session_state.suggestion_chosen: 
    for suggestion in suggestions: 
        if st.button(suggestion):
            st.session_state.suggestion_chosen = True
            # Add user message to chat history
            st.session_state.messages.append({"role": "user", "content": suggestion})
            
            # Display user input in chat message container
            with st.chat_message("user"):
                st.markdown(suggestion)  # Display the user's input 
            with st.spinner("Thinking..."):
                response = st.session_state.chatbot.get_gpt3_response(suggestion) 

            if isinstance(response, pd.DataFrame):
                st.dataframe(response)
                st.session_state.messages.append({"role": "assistant", "content": f"```{response.head(5)}```"})
            else:
                with st.chat_message("assistant"):
                    st.markdown(response)
                st.session_state.messages.append({"role": "assistant", "content": response})
                st.empty() # make the suggestion buttons disappear

### FEEDBACK ###
emoji_options = ["😀 Happy", "😐 Neutral", "😒 Dissatisfied", "😠 Angry"]

with st.sidebar:
    form_expander = st.expander("💭 Feedback", expanded=False)

# Feedback form
with form_expander:
    with st.form(key="feedback_form", clear_on_submit=True): 
        feedback_text = st.text_area(label="Please provide your feedback here:")
        selected_emoji = st.selectbox("How was your experience?", emoji_options)
        emoji_to_store = selected_emoji[0]
        submit_button = st.form_submit_button(label="Submit")

    if submit_button:
        # insert the time the feedback was submitted
        current_date = datetime.now().date()
        current_time = datetime.now().time()

        # Convert date and time to string format to store in Google Sheets
        current_date_str = current_date.isoformat()
        current_time_str = current_time.strftime('%H:%M:%S')

        client = init_google_sheets_client(json_credentials)
        sheet = client.open_by_url(spreadsheet_name).worksheet(worksheet_name)
        sheet.append_row([feedback_text, emoji_to_store, current_date_str, current_time_str])
        st.success("Feedback submitted successfully!")
        # all_values = sheet.get_all_values()
        # for row in all_values:
        #     print(row)

### ABOUT THE CHATBOT ###  
with st.sidebar:
    about_expander = st.expander("👋 About the chatbot", expanded=False)
    with about_expander:
        st.markdown(""" 
            <div class="text-container">
                <p style = "font-size: 0.9rem;">Welcome to our chatbot. Its role is to provide you with insights from the datasets available to it and make you understand the information they contain.</p>
                <p style = "font-size: 0.9rem;">The chatbot is capable of suggesting topics based on these datasets. It can also find datasets the best fit a topic or subject you are interested in and 
                provide you with insights about the data. You can check out the contents of the datasets and ask it to perform analytics operations on the data.</p>
                <p style = "font-size: 0.9rem;">Feel free to mess with the chatbot and experiment with it and don't forget to submit your opinion and feedback about it.</p>
            </div>
        """, unsafe_allow_html=True) 
