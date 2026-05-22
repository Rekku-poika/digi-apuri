import streamlit as st
import google.generativeai as genai
import datetime

if "GEMINI_KEY" not in st.secrets:
    st.error("API-avain puuttuu.")
    st.stop()

genai.configure(api_key=st.secrets["GEMINI_KEY"])
tanaan = datetime.date.today().strftime("%d.%m.%Y")

# Käytetään mallia gemini-1.5-flash-001
model = genai.GenerativeModel(model_name='gemini-1.5-flash-001')

if "messages" not in st.session_state: st.session_state.messages = []

st.title("🤖 Digi-Apuri")

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

if user_input := st.chat_input("Kirjoita viestisi..."):
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.write(user_input)

    try:
        # Haku yhdellä rivillä, joka toimii varmimmin
        response = model.generate_content(
            user_input,
            tools=["google_search_retrieval"]
        )
        vastaus = response.text
    except Exception as e:
        # Jos haku ei jostain syystä toimi, vastaa ilman sitä
        vastaus = model.generate_content(user_input).text

    with st.chat_message("assistant"):
        st.write(vastaus)
    st.session_state.messages.append({"role": "assistant", "content": vastaus})
    st.rerun()
