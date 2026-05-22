import streamlit as st
import google.generativeai as genai

# Aseta avain
genai.configure(api_key=st.secrets["GEMINI_KEY"])
model = genai.GenerativeModel('models/gemini-2.0-flash')

st.title("🤖 Digi-Apuri 2026")

if "messages" not in st.session_state: st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]): st.write(msg["content"])

if prompt := st.chat_input("Kysy jotain..."):
    st.chat_message("user").write(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    with st.chat_message("assistant"):
        try:
            response = model.generate_content(prompt)
            st.write(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error(f"Kiintiö täynnä tai virhe: {e}")
