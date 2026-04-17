import streamlit as st
import google.generativeai as genai

st.title("My Personal AI Chatbot")

# 1. Sabse pehle key check karte hain
api_key = st.secrets.get("GEMINI_API_KEY")

if not api_key:
    st.error("Bhai, Streamlit ko aapki Key nahi mil rahi. Secrets check karo.")
else:
    try:
        # 2. Key configure karein
        genai.configure(api_key=api_key)
        
        # 3. Naya model use karein (1.5-flash sabse fast hai)
        model = genai.GenerativeModel('gemini-1.5-flash-latest')
        
        user_input = st.text_input("Kuch puchiye:", key="input")
        
        if user_input:
            response = model.generate_content(user_input)
            st.write(response.text)
            
    except Exception as e:
        # Ye line humein asli wajah batayegi
        st.error(f"Asli Technical Error ye hai: {e}")
