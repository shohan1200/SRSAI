# st_app.py - SRS.AI Chatbot (Clean and Stable Version)



import streamlit as st

from google import genai

from PIL import Image 



# --- ১. CONFIGURATION ---

LOGO_PATH = "srs_logo.png" 

SYSTEM_INSTRUCTION = "You are a helpful and friendly AI assistant named SRS.AI. Your creator is Sohan Sir. Address the user as Sohan and respond in Bengali. Keep the tone supportive."



# API Key লোড করার একমাত্র সঠিক পদ্ধতি

try:

    # Streamlit Secrets-এ সেট করা GEMINI_API_KEY লোড করা হচ্ছে

    API_KEY = st.secrets["AIzaSyAPWZx1rz_MtQeFemd4n7b56RSboBQTevE"] 

except:

    st.error("API Key not found. Please set GEMINI_API_KEY in Streamlit Secrets.")

    st.stop()



# --- ২. INITIALIZATION ---



# Chat Session Management 

if "chat" not in st.session_state:

    try:

        client = genai.Client(api_key=API_KEY)

        config = {"system_instruction": SYSTEM_INSTRUCTION}

        

        # সহজ চ্যাট সেশন (কোনো জটিল টুল ছাড়াই)

        st.session_state.chat = client.chats.create(

            model="gemini-2.5-flash",

            config=config

        )

    except Exception as e:

        st.error(f"Initialization Error: {e}. Please check your API Key.")

        st.stop()



# --- ৩. UI AND HISTORY ---



st.set_page_config(initial_sidebar_state="collapsed", layout="wide")

try:

    st.sidebar.image(LOGO_PATH, width=200, caption="SRS.AI") 

except:

    st.sidebar.title("🤖 SRS.AI")

st.title("Your Simple SRS.AI Chatbot")



if "messages" not in st.session_state:

    st.session_state.messages = []

    st.session_state.messages.append({"role": "assistant", "content": "Welcome to SRS.AI! I am a simple chatbot created by Sohan Sir. Ask me anything."})



for message in st.session_state.messages:

    if message["role"] != "system":

        with st.chat_message(message["role"]):

            st.markdown(message["content"])



# --- ৪. CHAT INPUT LOGIC ---



if prompt := st.chat_input("Ask SRS.AI..."):

    

    # ইউজার মেসেজ ডিসপ্লে

    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user"):

        st.markdown(prompt)



    # AI উত্তর জেনারেট করা

    with st.chat_message("assistant"):

        message_placeholder = st.empty()

        full_response = ""

        

        try:

            # শুধু টেক্সট পাঠানো, স্ট্রিমিং সহ

            response_stream = st.session_state.chat.send_message(prompt, stream=True)

            

            for chunk in response_stream:

                full_response += chunk.text

                message_placeholder.markdown(full_response + "▌") 



            message_placeholder.markdown(full_response) 



        except Exception as e:

            st.error(f"Sorry, a critical error occurred: {e}")

            full_response = "Sorry, I encountered an error while processing your request."

        

        st.session_state.messages.append({"role": "assistant", "content": full_response})