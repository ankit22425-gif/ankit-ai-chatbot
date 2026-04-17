import streamlit as st
import google.generativeai as genai

# Page configuration
st.set_page_config(page_title="My AI Chatbot", page_icon="🤖")
st.title("My Personal AI Chatbot")

# 1. Secrets se Key check karna
if "GEMINI_API_KEY" not in st.secrets:
    st.error("Secret 'GEMINI_API_KEY' nahi mili! Streamlit Settings > Secrets mein check karein.")
    st.stop()

api_key = st.secrets["GEMINI_API_KEY"]

try:
    # 2. AQ wali key ke liye 'rest' transport zaroori hai
    genai.configure(api_key=api_key, transport='rest')

    # 3. Model initialization
    model = genai.GenerativeModel('gemini-1.5-flash')

    # Session state for chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # 4. User input and Response
    if prompt := st.chat_input("Kuch puchiye..."):
        # User message
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Assistant response
        with st.chat_message("assistant"):
            try:
                # Direct generation
                response = model.generate_content(prompt)
                
                if response.text:
                    st.markdown(response.text)
                    st.session_state.messages.append({"role": "assistant", "content": response.text})
                else:
                    st.warning("Model ne koi jawab nahi diya. Key ya Safety settings check karein.")
            
            except Exception as e:
                # Detailed Error for debugging
                st.error(f"Technical Error: {e}")
                if "404" in str(e):
                    st.info("Tip: Model name match nahi kar raha. Requirements.txt check karein.")
                elif "401" in str(e):
                    st.info("Tip: API Key invalid hai. Nayi key try karein.")

except Exception as e:
    st.error(f"Setup Error: {e}")
    
   
