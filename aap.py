import streamlit as st
import google.generativeai as genai

st.title("My Personal AI Chatbot")

# Secrets se key lena
if "GEMINI_API_KEY" not in st.secrets:
    st.error("Secrets mein GEMINI_API_KEY nahi mili!")
else:
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)

    # Model define karna (Naya tareeka)
    # Agar 1.5-flash nahi chalta, toh 'gemini-1.0-pro' try karna
    model = genai.GenerativeModel('gemini-1.5-flash')

    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Chat history dikhane ke liye
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # User input
    if prompt := st.chat_input("Kuch puchiye..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            try:
                response = model.generate_content(prompt)
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            except Exception as e:
                st.error(f"Technical Error: {e}")
       
