import streamlit as st
from openai import OpenAI

st.title("My Personal AI Chatbot")

# Sidebar mein API key mangne ka option (Ya fir code mein hide karein)
client = OpenAI(api_key="YOUR_API_KEY")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Purani chat dikhane ke liye
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User input
if prompt := st.chat_input("Kaise help karu?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=st.session_state.messages
        )
        reply = response.choices[0].message.content
        st.markdown(reply)
    st.session_state.messages.append({"role": "assistant", "content": reply})