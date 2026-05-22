import streamlit as st
import google.generativeai as genai
import datetime

# 1. Konfigurointi
if "GEMINI_KEY" not in st.secrets:
    st.error("API-avain puuttuu.")
    st.stop()

genai.configure(api_key=st.secrets["GEMINI_KEY"])

# 2. Käytetään mallia gemini-3.5-flash (Uusin ja toimivin flash-malli)
model = genai.GenerativeModel(model_name='models/gemini-3.5-flash')

# 3. Chat-alustus
if "messages" not in st.session_state: st.session_state.messages = []

st.title("🤖 Digi-Apuri (2026)")

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# 4. Syöte ja Haku
if user_input := st.chat_input("Kirjoita viestisi..."):
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.write(user_input)

    # TÄSSÄ KORJAUS: Käytetään google_search -työkalua "tools"-listassa
    # Tämä on vuoden 2026 standarditapa
    try:
        response = model.generate_content(
            user_input,
            tools=[{"google_search": {}}]
        )
        vastaus = response.text
    except Exception as e:
        vastaus = f"Pahoittelut, tekninen virhe: {str(e)}"

    with st.chat_message("assistant"):
        st.write(vastaus)
    st.session_state.messages.append({"role": "assistant", "content": vastaus})
    st.rerun()
