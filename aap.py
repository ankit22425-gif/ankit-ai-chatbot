import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="My AI Chatbot", layout="centered")
st.title("🤖 My Personal AI Chatbot (Gemini)")

# 1. API Configuration
try:
        genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
except:
    st.error("Bhai, Secrets mein GEMINI_API_KEY nahi mili!")

# 2. Chat History
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 3. Chat Logic
if prompt := st.chat_input("Can I help you?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            # Sabse stable model use kar rahe hain
            model = genai.GenerativeModel('gemini-pro') 
            response = model.generate_content(prompt)
            
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            # Agar gemini-pro na chale toh flash try karega
            try:
                model = genai.GenerativeModel('gemini-1.5-flash')
                response = model.generate_content(prompt)
                st.markdown(response.text)
            except:
                st.error("Bhai, Google ke models connect nahi ho rahe. Ek baar API Key dobara check karo.")
          
