import streamlit as st
import google.generativeai as genai

# Page ki setting
st.set_page_config(page_title="My AI Chatbot", layout="centered")
st.title("🤖 My Personal AI Chatbot (Gemini)")

# 1. Gemini API Key configure karein (Streamlit Secrets se)
try:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
except:
    st.error("Bhai, Gemini API Key nahi mili! Streamlit Secrets check karo.")

# 2. Chat history maintain karne ke liye
if "messages" not in st.session_state:
    st.session_state.messages = []

# 3. Purani baatein (Messages) screen par dikhane ke liye
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 4. Chat input box (User ke liye)
if prompt := st.chat_input("Kaise help karu?"):
    # User ka message session mein save karo
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # 5. Gemini se jawab mangna
    with st.chat_message("assistant"):
        try:
            model = genai.GenerativeModel('gemini-pro')
            response = model.generate_content(prompt)
            
            bot_response = response.text
            st.markdown(bot_response)
            
            # Bot ka jawab bhi save karo
            st.session_state.messages.append({"role": "assistant", "content": bot_response})
        except Exception as e:
            st.error(f"Error aa raha hai bhai: {e}")
