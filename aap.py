import streamlit as st
import google.generativeai as genai

# Page setup
st.set_page_config(page_title="My AI Chatbot", page_icon="🤖")
st.title("My Personal AI Chatbot")

# 1. Secrets se API Key uthana
if "GEMINI_API_KEY" not in st.secrets:
    st.error("Bhai, Streamlit Secrets mein 'GEMINI_API_KEY' nahi mili. Pehle Settings mein ja kar add karo!")
    st.stop()

api_key = st.secrets["GEMINI_API_KEY"]

try:
    # 2. Gemini ko configure karna
    genai.configure(api_key=api_key)
    
    # 3. Model select karna (Stable version)
    # Agar ye error de, toh 'gemini-1.5-flash' ko 'gemini-pro' se badal dena
    model = genai.GenerativeModel('gemini-1.5-flash')

    # Chat history initialize karna
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Purani baatein screen par dikhana
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # 4. User se sawal lena
    if prompt := st.chat_input("Kuch puchiye..."):
        # User ka message dikhao
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # AI ka jawab generate karna
        with st.chat_message("assistant"):
            try:
                response = model.generate_content(prompt)
                full_response = response.text
                st.markdown(full_response)
                st.session_state.messages.append({"role": "assistant", "content": full_response})
            except Exception as e:
                st.error(f"Response error: {e}")
                st.info("Tip: Agar 'AQ' wali key se error aa raha hai, toh Google AI Studio se 'AIzaSy' wali key try karein.")

except Exception as e:
    st.error(f"Setup Error: {e}")
