import streamlit as st
from streamlit_chat import message
from utils import get_initial_message, get_chatgpt_response, update_chat
import os
from dotenv import load_dotenv
load_dotenv()
from openai import OpenAI
#from config import OPENAI_API_KEY
client = OpenAI(api_key = st.secrets["OPENAI_API_KEY"])
if client not in st.session_state:
    client = OpenAI(api_key = st.secrets["OPENAI_API_KEY"])

st.title("Welcome to AI Fitz")
st.subheader("Gym Trainer:")


# model = st.selectbox(
#     "Select a model",
#     ("gpt-3.5-turbo", "gpt-4")
# )

if 'generated' not in st.session_state:
    st.session_state['generated'] = []
if 'past' not in st.session_state:
    st.session_state['past'] = []

query = st.text_input("Query: ", key="input")

if 'messages' not in st.session_state:
    st.session_state['messages'] = get_initial_message()
 
if query:
    with st.spinner("generating..."):
        messages = st.session_state['messages']
        messages = update_chat(messages, "user", query)
        # st.write("Before  making the API call")
        # st.write(messages)
        response = get_chatgpt_response(messages,"gpt-3.5-turbo")
        messages = update_chat(messages, "assistant", response)
        #print(st.session_state['messages'])
        st.session_state.past.append(query)
        st.session_state.generated.append(response)
        
if st.session_state['generated']:

    for i in range(len(st.session_state['generated'])-1, -1, -1):
        message(st.session_state['past'][i], is_user=True, key=str(i) + '_user')
        message(st.session_state["generated"][i], key=str(i))

    # with st.expander("Show Messages"):
    #     st.write(messages)
        
