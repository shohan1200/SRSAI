# st_app.py - SRS.AI Chatbot (FINAL PUBLISH VERSION - Clean Structure)



import streamlit as st

from google import genai

from PIL import Image 

import time



# --- ১. CONFIGURATION (পরিবর্তন করুন) ---

LOGO_PATH = "srs_logo.png" 

API_KEY = "AIzaSyAPWZx1rz_MtQeFemd4n7b56RSboBQTevE" # ⚠️ API Key বসান

SYSTEM_INSTRUCTION = "You are a helpful and friendly AI assistant named SRS.AI. Your creator and developer is Sohan Sir. When the user asks 'Who made you?' or 'Who is your creator?', you must answer only: 'Sohan Sir created me, and I operate under his guidance.' You must always address the user as Sohan. You must respond in the language of the user's query, but your primary language is Bengali. Keep the tone supportive and conversational."



# --- ২. CORE FUNCTIONS ---



def initialize_chat_session(api_key):

    """API Client এবং চ্যাট সেশন শুরু করে।"""

    try:

        client = genai.Client(api_key=api_key) 

    except Exception as e:

        st.error(f"API Connection Error: {e}")

        st.stop()

        

    config = {

        "system_instruction": SYSTEM_INSTRUCTION

    }



    # Google Search Tool সহ চ্যাট সেশন শুরু করা

    chat = client.chats.create(

        model="gemini-2.5-flash",

        config=config,

        tools=[{"google_search": {}}] 

    )

    return client, chat



def clear_chat_history():

    """চ্যাট হিস্টরি মুছে নতুন সেশন শুরু করে।"""

    keys_to_delete = ["chat", "messages"]

    for key in keys_to_delete:

        if key in st.session_state:

            del st.session_state[key]

    st.session_state.clear()

    st.rerun() 



def load_history_and_welcome():

    """মেমরি লোড করে এবং স্বাগত বার্তা যোগ করে।"""

    if "messages" not in st.session_state:

        st.session_state.messages = []

        

        # API থেকে বিদ্যমান চ্যাট হিস্টরি লোড করা

        history_messages = st.session_state.chat.get_history()

        

        # স্বাগত বার্তা

        if not history_messages:

            welcome_message = "Welcome to SRS.AI! I am an advanced chatbot created by Sohan Sir. I can use Google Search. Please ask your question."

            st.session_state.messages.append({"role": "assistant", "content": welcome_message})

        

        for history_message in history_messages:

            role = "assistant" if history_message.role == "model" else "user"

            st.session_state.messages.append({"role": role, "content": history_message.parts[0].text})



# --- ৩. MAIN APP LOGIC ---



# 3.1: API Key চেক এবং ক্লায়েন্ট ইনিশিয়ালাইজেশন

if not API_KEY or API_KEY == "আপনার_API_Key_এখানে_বসবে":

    st.error("API Key is not set. Please provide your API_KEY.")

    st.stop()



if "client" not in st.session_state or "chat" not in st.session_state:

    client, chat = initialize_chat_session(API_KEY)

    st.session_state.client = client

    st.session_state.chat = chat



# 3.2: UI এবং সাইডবার সেটআপ

st.set_page_config(initial_sidebar_state="collapsed", layout="wide")

try:

    st.sidebar.image(LOGO_PATH, width=200, caption="SRS.AI") 

except:

    st.sidebar.title("🤖 SRS.AI")

st.sidebar.title("🤖 SRS.AI Assistant") 



uploaded_file = st.sidebar.file_uploader(

    "Upload Image (PNG, JPG, JPEG)", 

    type=["png", "jpg", "jpeg"]

)



st.sidebar.button("🗑️ নতুন সেশন শুরু করুন", on_click=clear_chat_history)



st.title("Your Personal AI Chatbot")



# 3.3: ইতিহাস লোড এবং ডিসপ্লে

load_history_and_welcome()



for message in st.session_state.messages:

    if message.get("role") != "system":

        with st.chat_message(message["role"]):

            st.markdown(message["content"])





# 3.4: ইউজার ইনপুট এবং রেস্পন্স জেনারেশন

if prompt := st.chat_input("Ask SRS.AI..."):

    

    # কন্টেন্ট প্রস্তুত

    contents = []

    if uploaded_file is not None:

        try:

            image = Image.open(uploaded_file)

            contents.append(image)

        except Exception as e:

            st.error(f"Error loading image: {e}")

            st.stop()

        

    contents.append(prompt)

    

    # ইউজার মেসেজ ডিসপ্লে

    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user"):

        st.markdown(prompt)

        if uploaded_file is not None:

            st.image(image, caption=f"Uploaded: {uploaded_file.name}", width=200)



    # অ্যাসিস্ট্যান্ট রেস্পন্স (স্ট্রিমিং সহ)

    with st.chat_message("assistant"):

        message_placeholder = st.empty()

        full_response = ""

        

        try:

            response_stream = st.session_state.chat.send_message(contents, stream=True)

            

            for chunk in response_stream:

                full_response += chunk.text

                message_placeholder.markdown(full_response + "▌") 



            message_placeholder.markdown(full_response) 



        except Exception as e:

            st.error(f"Sorry, a critical error occurred: {e}")

            full_response = "Sorry, I encountered an error while processing your request."

        

        # চূড়ান্ত উত্তর ইতিহাস আপডেট করা

        st.session_state.messages.append({"role": "assistant", "content": full_response})