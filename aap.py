import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="My AI Chatbot", layout="centered")
st.title("🤖 My Personal AI Chatbot (Gemini)")

try:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
except:
    st.error("Bhai, Gemini API Key nahi mili!")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Kaise help karu?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            # Yahan humne model ka naam 'gemini-pro' kar diya hai jo sabse stable hai
            model = genai.GenerativeModel('gemini-pro') 
            response = model.generate_content(prompt)
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error(f"Error aa raha hai bhai: {e}")
